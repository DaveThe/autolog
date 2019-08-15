from __future__ import print_function, unicode_literals

import argparse
import csv
import io
import json
import logging
import os
import re
import signal
import string
import subprocess
import sys
import time
from glob import glob

import bluetooth
import obd
import serial
from examples import custom_style_1
from obd import OBDCommand, OBDStatus, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int
from pyfiglet import Figlet
from PyInquirer import Token, print_json, prompt, style_from_dict

from assets import blacklisted_pids, ecu
from command import get_date
from playground import while_cmd
from questions import *

"""
OBD EMULATOR
https://github.com/Ircama/ELM327-emulator
"""


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# logging.basicConfig(level=logging.DEBUG)

logging.basicConfig(
    level=logging.NOTSET,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(CURRENT_DIR+"/logs/", f"{get_date()}")),
        logging.StreamHandler()
    ])

logger = logging.getLogger(__name__)


def main():

    f = Figlet(font="banner3-D")
    logger.info(f.renderText("Auto  Log"))

    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(
        epilog='CarMonitor obd data ingestion.')

    parser.add_argument(
        '-b',
        "--batch",
        dest='batch',
        action='store_true',
        help="get config from default")

    args = parser.parse_args()

    if not args.batch:
        logger.info("Car Monitor run in batch")
        go_answers = prompt(continue_question, style=custom_style_1)
        if go_answers['continue']:
            answers = prompt(general_questions, style=custom_style_1)
            logger.debug(answers)
        else:
            exit()
    else:
        answers = {'enviroment': 'prod', 'port': 'rfcomm0', 'pairing': False}
        go_answers = {'continue': True}

    device_json = {}
    if answers['pairing']:
        device = get_nearby_devices()
        if device:
            address = device[0]
            name = device[1]
            device_json = {
                "address": address,
                "name": name
            }
            logger.debug(device_json)
            with open(CURRENT_DIR+'/device.cfg', 'w') as outfile:
                json.dump(device_json, outfile)

            port = 0         # RFCOMM port
            passkey = "1111"  # passkey of the device you want to connect

            # kill any "bluetooth-agent" process that is already running
            subprocess.call("kill -9 `pidof bluetooth-agent`", shell=True)

            # Start a new "bluetooth-agent" process where XXXX is the passkey
            status = subprocess.call("bluetooth-agent " + passkey + " &", shell=True)

            # Now, connect in the same way as always with PyBlueZ
            try:
                s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                s.connect((address, port))
            except bluetooth.btcommon.BluetoothError as err:
                # Error handler
                logger.exception(err)
                pass
    else:
        logger.info("get config from file")
        with open(CURRENT_DIR+'/device.cfg') as json_file:
            device_json = json.load(json_file)

    logger.debug(device_json)

    obd.logger.setLevel(obd.logging.DEBUG)
    connection = connect_to_car(answers)
    conn_status = connection.status()
    # a callback that prints every new value to the console

    logger.info(conn_status)
    try:
        if conn_status == OBDStatus.CAR_CONNECTED:
            logger.info(connection.protocol_name())
            pids_list = get_pids_list()
            logger.info(f"STANDARD PIDS # {len(connection.supported_commands)}")
            time.sleep(2)
            if pids_list:
                for csv_pid in pids_list:
                    with open(csv_pid, 'rt') as csv_file:
                        logger.info(f"csv path {csv_pid}")
                        connection = custom_pids_handler(obd_connection=connection,
                                                         csv_file=csv_file)

            logger.info(f"AFTER CUSTOM PIDS # {len(connection.supported_commands)}")

            while_cmd(connection, get_date())
        elif conn_status == OBDStatus.OBD_CONNECTED:
            logger.warning("""successful communication with the ELM327 adapter,
            # OBD port connected to the car, ignition off
            # (not available with argument "check_voltage=False")""")
        else:
            retry_answers = prompt(retry_question, style=custom_style_1)
            if retry_answers['retry']:
                connection = get_obd_connection(answers)
    except ConnectionError as ex:
        logger.exception("ERRORE!!")
        logger.exception(ex)
        connection.stop()


def get_nearby_devices():
    logger.info("Start Searching nearby devices")
    nearby_devices = bluetooth.discover_devices(duration=4, lookup_names=True,
                                                flush_cache=True, lookup_class=False)

    logger.debug(nearby_devices)
    nearby_devices_list = []
    if nearby_devices:
        for raw_list in nearby_devices:
            nearby_devices_list.append(raw_list[1])

        logger.debug(nearby_devices_list)

        nearby_devices_questions = [
            {
                'type': 'rawlist',
                'name': 'bluetooth_device',
                'message': 'Select the OBD device',
                'choices': nearby_devices_list
            }
        ]
        devices_answers = prompt(nearby_devices_questions, style=style)

        logger.info(f"devices_answers - {devices_answers}")
        selected = devices_answers['bluetooth_device']
        logger.info(f"device selected {selected}")
        device = [item for item in nearby_devices if item[1] == selected][0]
        logger.info(f"device details {device}")
        return device
    else:
        logger.info("no device found!")
        return None


def signal_handler(sig, frame):
    # print('You pressed Ctrl+C!')
    exit_answers = prompt(exit_question, style=style)
    if exit_answers['exit']:
        f = Figlet(font="banner3-D")
        logger.info(f.renderText("Bye Bye"))
        sys.exit(0)


def get_pids_list():
    PATH = CURRENT_DIR+"/pids"
    EXT = "*.csv"
    all_csv_files = [file
                     for path, subdir, files in os.walk(PATH)
                     for file in glob(os.path.join(path, EXT))]
    logger.debug(all_csv_files)
    return all_csv_files


def connect_to_car(answers):
    retry = 1
    conn_status = ''
    while retry < 4 and conn_status is not OBDStatus.CAR_CONNECTED:
        logger.info(f"retry counts #{retry} and connection status: {conn_status}")
        connection = get_obd_connection(answers)
        conn_status = connection.status()
        logger.info(f"connection protocol: {connection.protocol_name()}")
        retry += 1
    return connection


def get_obd_connection(answers):
    logger.info(f"port - {answers['port']}")
    if answers['enviroment'] == "debug":
        connection = obd.OBD("/dev/pts/3")
        obd.logger.setLevel(obd.logging.DEBUG)
    else:
        os.system('sudo rfcomm bind hci0 00:0D:18:3A:67:89 1')
        connection = obd.OBD("/dev/rfcomm0", fast=False, timeout=30)
        obd.logger.setLevel(obd.logging.INFO)

    return connection


def add_at(data):
    stack = 0
    startIndex = 0
    stackbreak = 0
    for i, c in enumerate(data):
        if c == '{':
            if stack == 1 and re.search("'AT'[ \t]*:", data[startIndex:i]):
                startIndex = i + 1
                stackbreak = stack
            stack += 1
        elif c == '}':
            stack -= 1
            if stack == stackbreak:
                break

    if stack == 1 and i > startIndex + 1:
        try:
            print('        ' + data[startIndex:i].strip())
        except:
            obd.logger.error("Malformed 'AT' scenario in input file")
    else:
        obd.logger.error("'AT' scenario not found in input file")


def custom_pids_handler(obd_connection, csv_file, probes=10, with_blacklist=False,
                        delay_commands=0, delay=0, dictionary_out=0,
                        car_name="default-car", at=0, print_missing_resp=0):

    SEP = '|'
    obd.logger.info("Reading CSV file...")
    reader = csv.reader(csv_file)
    custom_pids = list(reader)
    for i in custom_pids:
        if i[0] == 'Name' or len(i) != 8 or not i[7] in ecu:
            if i[0] != 'Name':
                if len(i) == 8 and not i[7] in ecu:
                    obd.logger.error("Unknown ECU " + repr(i[7]) +
                                     " in CSV line " + repr(i))
                else:
                    obd.logger.error("Invalid CSV data: " + repr(i))
            continue
        Pid = 'CUSTOM_' + i[1].upper().replace(' ', '_')
        Descr = i[0] + SEP + i[3] + SEP + i[4] + SEP + i[5] + SEP + i[6]
        Request = i[2].strip()
        Header = i[7]
        obd_connection.supported_commands.add(
            OBDCommand(
                Pid,
                Descr,
                Request.encode(),
                0,
                lambda messages: "\n".join([m.raw() for m in messages]),
                ECU.ALL,
                True,
                header=Header.encode()))
    obd.logger.info("CSV file processing complete")

    # Query all commands in the dictionary and return responses to OBDData
    OBDData = [dict() for x in range(probes)]
    for i in range(probes):
        obd.logger.info("Start probe number: " + str(i))
        for cmd in obd_connection.supported_commands:
            cmd.ecu = ECU.ALL
            if cmd.name not in blacklisted_pids or with_blacklist:
                OBDData[i][cmd] = obd_connection.query(cmd)
                time.sleep(delay_commands)
        time.sleep(delay)
    obd.logger.info("End of probing process. Producing dictionary...")

    # Sort the list of supported commands
    l = list(obd_connection.supported_commands)
    l.sort(
        key=lambda cmd: ('0' if cmd.name.startswith('ELM_')
                         else '2' if cmd.name.startswith('CUSTOM_')
                         else '1') +
        SEP + (ecu[cmd.header.decode()]
               if cmd.header.decode() in ecu else cmd.header.decode()) +
        SEP + cmd.command.decode())

    # Redirect stdout
    if dictionary_out:
        sys.stdout = dictionary_out[0]

    # Print header information
    logger.debug("\n".join([ecu[k] + ' = "' + k + '"' for k in ecu]))
    logger.debug('ELM_R_OK = "OK\\r"\nELM_MAX_RESP = "[0123456]?$"\n')
    logger.debug("ObdMessage = {")
    logger.debug("    '" + car_name + "': {")

    # Loop all sorted commands
    cmd_type = 0
    for cmd in l:
        if cmd.name.startswith('CUSTOM_') and cmd_type != 3:
            logger.debug('    # Custom OBD Commands')
            cmd_type = 3
        elif cmd.name.startswith('ELM_') and cmd_type != 2:
            logger.debug('    # AT Commands')
            cmd_type = 2
            if at:
                add_at(at.read())
        elif not cmd.name.startswith('CUSTOM_') and not cmd.name.startswith(
                'ELM_') and cmd_type != 1:
            logger.debug('    # OBD Commands')
            cmd_type = 1

        # for each command, generate the lists of responses and values
        list_resp = []
        list_vals = {}  # dict of available values for each list_resp
        for response in [d[cmd] for d in OBDData if cmd in d]:
            if not response.messages:
                obd.logger.info('No data for PID %s (%s)' % (
                    repr(cmd.name), repr(cmd.command)))
                continue
            p_resp = ''
            for i in response.messages:
                for r in i.raw().splitlines():
                    h = r[:3]  # header
                    if len(r) > 4 and h in ecu and re.match('^[0-9a-fA-F\r\n]*$', r):
                        s = r[3:]  # bytes
                        p = " ".join(s[i:i + 2]
                                     for i in range(0, len(s), 2))  # spaced bytes
                        p_resp += (" +\n                        " if p_resp
                                   else '') + ecu[h] + " + ' " + p + " \\r'"
                    else:  # word (not string of bytes)
                        p_resp += (" +\n                        "
                                   if p_resp else '') + "'" + r\
                            .replace('"', "\\\\'")\
                            .replace("'", "\\\'") + " \\r'"
            if p_resp:
                list_resp.append(p_resp)
                if response.value and hasattr(response.value, 'magnitude'):
                    list_vals[p_resp] = '{!s}'.format(response.value)\
                        .replace('"', "\\'")\
                        .replace("'", "\\'")

        # discard PIDs with missing response
        if not list_resp:
            if not with_blacklist and cmd.name in blacklisted_pids:
                obd.logger.debug('Blacklisted PID %s (%s)' % (
                    repr(cmd.name), repr(cmd.command)))
            else:
                obd.logger.error('No response data for PID %s, %s (%s)' % (
                    repr(cmd.name), repr(cmd.desc), repr(cmd.command)))
                if print_missing_resp:
                    logger.debug('        # No response data for PID %s, %s (%s)' % (
                        repr(cmd.name), repr(cmd.desc), repr(cmd.command)))
            continue

        # discard duplicates
        list_resp = list(set(list_resp))

        # produce the final printable strings of responses and values
        if len(list_resp) > 1:
            f_resp = ('[\n                        ' +
                      ',\n                        '.join(list_resp) +
                      '\n                        ]')
        else:
            f_resp = next(iter(list_resp))
        f_val = "\n            # ".join(
            [list_vals[x] for x in list_resp if x in list_vals])

        # print all data
        logger.debug("        " + repr(cmd.name) + ": {")
        logger.debug("            'Request': '^" + cmd.command.decode() +
                     "' + ELM_MAX_RESP,")
        descr_list = cmd.desc.split(SEP)
        logger.debug("            'Descr': '" + descr_list[0] + "',")
        if len(descr_list) >= 5:
            logger.debug("            'Equation': '" + descr_list[1] + "',")
            logger.debug("            'Min': '" + descr_list[2] + "',")
            logger.debug("            'Max': '" + descr_list[3] + "',")
            logger.debug("            'Unit': '" + descr_list[4] + "',")
            logger.debug("            'Header': " + ecu[cmd.header.decode()] + ","
                         if cmd.header.decode() in ecu else cmd.header.decode() + ",")
        logger.debug("            'Response': " + f_resp)
        if f_val:
            logger.debug("            # " + f_val)
        logger.debug("        },")
    logger.debug("    },")
    logger.debug("}")
    obd.logger.info("Dictionary production complete.")

    return obd_connection


main()
