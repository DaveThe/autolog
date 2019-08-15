import datetime
import os

import pytz

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def new_rpm(r):
    print(r.value)


def get_date():
    d = datetime.datetime.now()  # .isoformat()
    timezone = pytz.timezone("Europe/Rome")
    d_aware = timezone.localize(d)
    print(d_aware)
    print(d_aware.isoformat())
    return d_aware.isoformat()


def save_param(fuel_level, speed, air_temp):
    # datetime.datetime.now().isoformat()
    row = str(fuel_level) + "," + str(speed) + "," + str(air_temp) + ","+get_date() + "\n"
    print(row)

    with open("obd_data_rows.txt", "a+") as f_g:
        f_g.write(row)


def save_args(*argv, name_log):
    row = ', '.join(map(str, argv))

    with open(CURRENT_DIR+"/obd_results/"+name_log+".txt", "a+") as f_g:
        f_g.write(row + "\n")


def save_kargs(**kwargs):

    data = {}
    for key, value in kwargs.items():

        if key not in data:
            data[key] = []
        data[key].append(value)
        print("%s == %s" % (key, value))
        with open("obd_data_rows_new.txt", "a+") as f_g:
            f_g.write(str(key) + " | " + str(value) + "\n")
