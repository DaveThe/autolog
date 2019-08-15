import pandas as pd
import json
file = open("/home/davide/Downloads/obd_data_rows_new_3.txt", "r")

data = {}
datas = []
for line in file:
    dat = line.split("|")
    # print(dat)
    key = dat[0].replace("\n", "").strip()
    value = dat[1]
    if key not in data:
        data[key] = []
    data[key].append(value)
    datas.append({key: value})

# print(json.dumps(data))
# print(data['DTC_WARMUPS_SINCE_DTC_CLEAR'])
# pandas.read_json(datas)
for da in data:
    if len(data[da]) == 74:
        print(da)
        data[da].append("None")
        # print(da + " - " + str(data[da]))

with open("obd_data_rows_new.json", "a+") as f_g:
    f_g.write(json.dumps(data))

df = pd.DataFrame(data)
df.to_csv("/home/davide/Downloads/obd_data_rows_new_3.csv")
