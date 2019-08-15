import time
import logging

import obd
from obd.protocols import ECU

from assets import blacklisted_pids, ecu
from command import get_date, new_rpm, save_args, save_kargs, save_param


logger = logging.getLogger(__name__)


def while_cmd(connection, name_log, delay_commands=0, delay=5):
    save_args(blacklisted_pids, name_log="blacklisted_pids-"+name_log)
    while True:
        OBDData = []
        for cmd in connection.supported_commands:
            save_args(cmd.name, name_log="commands-"+name_log)
            cmd.ecu = ECU.ALL
            if cmd.name not in blacklisted_pids:
                response = connection.query(cmd)
                OBDData.append(response)
                command_name = response.command
                logger.info(command_name)
                if not response.is_null():
                    command_value = response.value
                    logger.info(response.value)
                    save_kargs(COMMAND_NAME=command_name, VALUE=command_value, MESSAGES=response.messages,
                               TIME=response.time, RAW=response, name_log=name_log)
                    save_args(command_name, command_value, response.messages,
                              response.time, response, name_log=name_log)
                time.sleep(delay_commands)
        save_args(OBDData, name_log="raw-"+name_log)
        time.sleep(delay)
        """
        save_kargs(MONITOR_VVT_B1=connection.query(obd.commands.MONITOR_VVT_B1),
                   SHORT_FUEL_TRIM_1=connection.query(obd.commands.SHORT_FUEL_TRIM_1),
                   LONG_FUEL_TRIM_1=connection.query(obd.commands.LONG_FUEL_TRIM_1),
                   ENGINE_LOAD=connection.query(obd.commands.ENGINE_LOAD),
                   COOLANT_TEMP=connection.query(obd.commands.COOLANT_TEMP),
                   FUEL_STATUS=connection.query(obd.commands.FUEL_STATUS),
                   PIDS_A=connection.query(obd.commands.PIDS_A),
                   STATUS=connection.query(obd.commands.STATUS),
                   INTAKE_TEMP=connection.query(obd.commands.INTAKE_TEMP),
                   SPEED=connection.query(obd.commands.SPEED),
                   TIMING_ADVANCE=connection.query(obd.commands.TIMING_ADVANCE),
                   INTAKE_PRESSURE=connection.query(obd.commands.INTAKE_PRESSURE),
                   RPM=connection.query(obd.commands.RPM),
                   ELM_VOLTAGE=connection.query(obd.commands.ELM_VOLTAGE),
                   DTC_STATUS_DRIVE_CYCLE=connection.query(obd.commands.DTC_STATUS_DRIVE_CYCLE),
                   DTC_PIDS_C=connection.query(obd.commands.DTC_PIDS_C),
                   DTC_ABSOLUTE_LOAD=connection.query(obd.commands.DTC_ABSOLUTE_LOAD),
                   DTC_CONTROL_MODULE_VOLTAGE=connection.query(obd.commands.DTC_CONTROL_MODULE_VOLTAGE),
                   DTC_RELATIVE_THROTTLE_POS=connection.query(obd.commands.DTC_RELATIVE_THROTTLE_POS),
                   DTC_COMMANDED_EQUIV_RATIO=connection.query(obd.commands.DTC_COMMANDED_EQUIV_RATIO),
                   DTC_THROTTLE_POS_B=connection.query(obd.commands.DTC_THROTTLE_POS_B),
                   DTC_AMBIANT_AIR_TEMP=connection.query(obd.commands.DTC_AMBIANT_AIR_TEMP),
                   DTC_ACCELERATOR_POS_D=connection.query(obd.commands.DTC_ACCELERATOR_POS_D),
                   ELM_VERSION=connection.query(obd.commands.ELM_VERSION),
                   MONITOR_MISFIRE_CYLINDER_4=connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_4),
                   MONITOR_O2_HEATER_B1S1=connection.query(obd.commands.MONITOR_O2_HEATER_B1S1),
                   MIDS_C=connection.query(obd.commands.MIDS_C),
                   MONITOR_O2_HEATER_B1S2=connection.query(obd.commands.MONITOR_O2_HEATER_B1S2),
                   SHORT_O2_TRIM_B1=connection.query(obd.commands.SHORT_O2_TRIM_B1),
                   LONG_O2_TRIM_B1=connection.query(obd.commands.LONG_O2_TRIM_B1),
                   FUEL_TYPE=connection.query(obd.commands.FUEL_TYPE),
                   MONITOR_CATALYST_B1=connection.query(obd.commands.MONITOR_CATALYST_B1),
                   MIDS_B=connection.query(obd.commands.MIDS_B),
                   FUEL_RAIL_PRESSURE_ABS=connection.query(obd.commands.FUEL_RAIL_PRESSURE_ABS),
                   DTC_FUEL_RAIL_PRESSURE_ABS=connection.query(obd.commands.DTC_FUEL_RAIL_PRESSURE_ABS),
                   DTC_LONG_O2_TRIM_B1=connection.query(obd.commands.DTC_LONG_O2_TRIM_B1),
                   DTC_SHORT_O2_TRIM_B1=connection.query(obd.commands.DTC_SHORT_O2_TRIM_B1),
                   DTC_FUEL_TYPE=connection.query(obd.commands.DTC_FUEL_TYPE),
                   DTC_ACCELERATOR_POS_E=connection.query(obd.commands.DTC_ACCELERATOR_POS_E),
                   DTC_THROTTLE_ACTUATOR=connection.query(obd.commands.DTC_THROTTLE_ACTUATOR),
                   DTC_TIME_SINCE_DTC_CLEARED=connection.query(obd.commands.DTC_TIME_SINCE_DTC_CLEARED),
                   DTC_RUN_TIME_MIL=connection.query(obd.commands.DTC_RUN_TIME_MIL),
                   CLEAR_DTC=connection.query(obd.commands.CLEAR_DTC),
                   GET_CURRENT_DTC=connection.query(obd.commands.GET_CURRENT_DTC),
                   GET_DTC=connection.query(obd.commands.GET_DTC),
                   CONTROL_MODULE_VOLTAGE=connection.query(obd.commands.CONTROL_MODULE_VOLTAGE),
                   ABSOLUTE_LOAD=connection.query(obd.commands.ABSOLUTE_LOAD),
                   PIDS_C=connection.query(obd.commands.PIDS_C),
                   STATUS_DRIVE_CYCLE=connection.query(obd.commands.STATUS_DRIVE_CYCLE),
                   AMBIANT_AIR_TEMP=connection.query(obd.commands.AMBIANT_AIR_TEMP),
                   THROTTLE_POS_B=connection.query(obd.commands.THROTTLE_POS_B),
                   COMMANDED_EQUIV_RATIO=connection.query(obd.commands.COMMANDED_EQUIV_RATIO),
                   RELATIVE_THROTTLE_POS=connection.query(obd.commands.RELATIVE_THROTTLE_POS),
                   ACCELERATOR_POS_D=connection.query(obd.commands.ACCELERATOR_POS_D),
                   DTC_DISTANCE_W_MIL=connection.query(obd.commands.DTC_DISTANCE_W_MIL),
                   DTC_PIDS_B=connection.query(obd.commands.DTC_PIDS_B),
                   MONITOR_MISFIRE_CYLINDER_1=connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_1),
                   MONITOR_MISFIRE_CYLINDER_2=connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_2),
                   MIDS_F=connection.query(obd.commands.MIDS_F),
                   MONITOR_MISFIRE_GENERAL=connection.query(obd.commands.MONITOR_MISFIRE_GENERAL),
                   CATALYST_TEMP_B1S2=connection.query(obd.commands.CATALYST_TEMP_B1S2),
                   CATALYST_TEMP_B1S1=connection.query(obd.commands.CATALYST_TEMP_B1S1),
                   DTC_CATALYST_TEMP_B1S1=connection.query(obd.commands.DTC_CATALYST_TEMP_B1S1),
                   DTC_CATALYST_TEMP_B1S2=connection.query(obd.commands.DTC_CATALYST_TEMP_B1S2),
                   MONITOR_O2_B1S1=connection.query(obd.commands.MONITOR_O2_B1S1),
                   MIDS_A=connection.query(obd.commands.MIDS_A),
                   MONITOR_O2_B1S2=connection.query(obd.commands.MONITOR_O2_B1S2),
                   O2_S1_WR_CURRENT=connection.query(obd.commands.O2_S1_WR_CURRENT),
                   BAROMETRIC_PRESSURE=connection.query(obd.commands.BAROMETRIC_PRESSURE),
                   DISTANCE_SINCE_DTC_CLEAR=connection.query(obd.commands.DISTANCE_SINCE_DTC_CLEAR),
                   WARMUPS_SINCE_DTC_CLEAR=connection.query(obd.commands.WARMUPS_SINCE_DTC_CLEAR),
                   DTC_WARMUPS_SINCE_DTC_CLEAR=connection.query(obd.commands.DTC_WARMUPS_SINCE_DTC_CLEAR),
                   DTC_DISTANCE_SINCE_DTC_CLEAR=connection.query(obd.commands.DTC_DISTANCE_SINCE_DTC_CLEAR),
                   DTC_BAROMETRIC_PRESSURE=connection.query(obd.commands.DTC_BAROMETRIC_PRESSURE),
                   DTC_O2_S1_WR_CURRENT=connection.query(obd.commands.DTC_O2_S1_WR_CURRENT),
                   DTC_COMMANDED_EGR=connection.query(obd.commands.DTC_COMMANDED_EGR),
                   DTC_FUEL_LEVEL=connection.query(obd.commands.DTC_FUEL_LEVEL),
                   DTC_EVAPORATIVE_PURGE=connection.query(obd.commands.DTC_EVAPORATIVE_PURGE),
                   DTC_EGR_ERROR=connection.query(obd.commands.DTC_EGR_ERROR),
                   THROTTLE_ACTUATOR=connection.query(obd.commands.THROTTLE_ACTUATOR),
                   ACCELERATOR_POS_E=connection.query(obd.commands.ACCELERATOR_POS_E),
                   RUN_TIME_MIL=connection.query(obd.commands.RUN_TIME_MIL),
                   TIME_SINCE_DTC_CLEARED=connection.query(obd.commands.TIME_SINCE_DTC_CLEARED),
                   DTC_COOLANT_TEMP=connection.query(obd.commands.DTC_COOLANT_TEMP),
                   DTC_ENGINE_LOAD=connection.query(obd.commands.DTC_ENGINE_LOAD),
                   DTC_LONG_FUEL_TRIM_1=connection.query(obd.commands.DTC_LONG_FUEL_TRIM_1),
                   DTC_SHORT_FUEL_TRIM_1=connection.query(obd.commands.DTC_SHORT_FUEL_TRIM_1),
                   DTC_STATUS=connection.query(obd.commands.DTC_STATUS),
                   DTC_FUEL_STATUS=connection.query(obd.commands.DTC_FUEL_STATUS),
                   PIDS_B=connection.query(obd.commands.PIDS_B),
                   DISTANCE_W_MIL=connection.query(obd.commands.DISTANCE_W_MIL),
                   OBD_COMPLIANCE=connection.query(obd.commands.OBD_COMPLIANCE),
                   RUN_TIME=connection.query(obd.commands.RUN_TIME),
                   DTC_OBD_COMPLIANCE=connection.query(obd.commands.DTC_OBD_COMPLIANCE),
                   DTC_RUN_TIME=connection.query(obd.commands.DTC_RUN_TIME),
                   MIDS_E=connection.query(obd.commands.MIDS_E),
                   DTC_O2_SENSORS=connection.query(obd.commands.DTC_O2_SENSORS),
                   DTC_MAF=connection.query(obd.commands.DTC_MAF),
                   DTC_THROTTLE_POS=connection.query(obd.commands.DTC_THROTTLE_POS),
                   DTC_O2_B1S2=connection.query(obd.commands.DTC_O2_B1S2),
                   MONITOR_MISFIRE_CYLINDER_3=connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_3),
                   MIDS_D=connection.query(obd.commands.MIDS_D),
                   THROTTLE_POS=connection.query(obd.commands.THROTTLE_POS),
                   MAF=connection.query(obd.commands.MAF),
                   O2_SENSORS=connection.query(obd.commands.O2_SENSORS),
                   O2_B1S2=connection.query(obd.commands.O2_B1S2),
                   EGR_ERROR=connection.query(obd.commands.EGR_ERROR),
                   EVAPORATIVE_PURGE=connection.query(obd.commands.EVAPORATIVE_PURGE),
                   FUEL_LEVEL=connection.query(obd.commands.FUEL_LEVEL),
                   COMMANDED_EGR=connection.query(obd.commands.COMMANDED_EGR),
                   DTC_TIMING_ADVANCE=connection.query(obd.commands.DTC_TIMING_ADVANCE),
                   DTC_SPEED=connection.query(obd.commands.DTC_SPEED),
                   DTC_INTAKE_TEMP=connection.query(obd.commands.DTC_INTAKE_TEMP),
                   MONITOR_EGR_B1=connection.query(obd.commands.MONITOR_EGR_B1),
                   DTC_RPM=connection.query(obd.commands.DTC_RPM),
                   DTC_INTAKE_PRESSURE=connection.query(obd.commands.DTC_INTAKE_PRESSURE),
                   TIMESTAMP=get_date())
        """
        """
        save_param(connection.query(obd.commands.FUEL_LEVEL),
                connection.query(obd.commands.SPEED),
                connection.query(obd.commands.DTC_AMBIANT_AIR_TEMP))
        # non-blocking, returns immediately
        """
        # the callback will now be fired upon receipt of new values

        # time.sleep(5)
