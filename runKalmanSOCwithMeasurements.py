#This Script 
  # 1.gets the measurement data from influxdb
  # 1.1. struct it as follows row1: batteryMilliAmps,	batteryMilliWatts,	isBatteryInFloat,	batteryVoltage,	samplePeriodMilliSec,	timestamp, therest
  # 1.2. write to /data/raw_sensor_data.csv
  # 2.Executes ./backtest
  # 3.Reads the calculated SOC from the /data/processed_sensor_data.csv
  # 4.Writes it into the influxdb on the correct place. 
 

#requirements: python3 -m pip install influxdb ? 
import os 
import subprocess
import pandas as pd
from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client .client.write_api import SYNCHRONOUS


bucket ="LabjackCurrentVoltage"
org ="LibreSolar"
token ="environement-variable"
url="https://influxdb.lsserver.uber.space"
toMilli = 1000



client = InfluxDBClient(
   url=url,
   token=token,
   org=org
)
# |> range(start: -97d, stop: -95d)
query_api = client.query_api()
query = 'from(bucket:"LabjackCurrentVoltage")\
|> range(start: 2021-05-28T20:10:00.000Z, stop: 2021-05-29T02:19:00.000Z)\
|> filter(fn: (r) => r["_measurement"] == "V" or r["_measurement"] == "A" or r["_measurement"] == "Info")\
|> filter(fn: (r) => r["_field"] == "Bat_V" or r["_field"] == "Bat_A" or r["_field"] == "ChgState" or r["_field"] == "SOC_pct")\
|> filter(fn: (r) => r["device"] == "mppt-1210-hus")'
# do structing with flux seems inefficient (>8s)
#|> group(columns: ["_time"])'
#|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'


#csv_result = query_api.query_csv(query,dialect=Dialect(header=False, delimiter=",", comment_prefix="#", annotations=[],date_time_format="RFC3339"))

df_query= client.query_api().query_data_frame(org=org, query=query)
print(df_query)

df_query = df_query.pivot(index = '_time',columns = '_field', values='_value').reset_index()
print(df_query)

df_query = df_query[['Bat_A', 'ChgState','Bat_V','_time','SOC_pct']] # reorder column to:
#batteryMilliAmps,	batteryMilliWatts,	isBatteryInFloat,	 batteryVoltage,	samplePeriodMilliSec	 timestamp
df_query["Bat_A"] = toMilli * df_query["Bat_A"]
df_query["Bat_V"] = toMilli * df_query["Bat_V"]
df_query.insert(1, "batteryMilliWatts",df_query['Bat_A'] * df_query['Bat_V'] , True)
df_query.insert(4, "samplePeriodMilliSec", '1' , True)
df_query = df_query.rename(columns={"Bat_A": "batteryMilliAmps", "batteryMilliWatts": "batteryMilliWatts","ChgState": "isBatteryInFloat", "Bat_V": "batteryVoltage", "samplePeriodMilliSec" : "samplePeriodMilliSec", "_time": "timestamp"})
df_query = df_query.astype({'batteryMilliAmps' : 'int32',	'batteryMilliWatts' : 'int32','isBatteryInFloat': 'int32',	 'batteryVoltage': 'int32',	'samplePeriodMilliSec': 'int32'})
print(df_query)
print(df_query.info())

df_query.to_csv(os.getcwd()+'/data/raw_sensor_data.csv',index=False)

subprocess.run("./backtest",cwd =os.getcwd()+"/builddir/")

#write_api = client.write_api(write_options=SYNCHRONOUS)

#p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
#write_api.write(bucket=bucket, org=org, record=p)


"""
Close client
"""
client.close()

# with open('raw_sensor_data.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerows(csv_result)


#from(bucket:"LabjackCurrentVoltage")
# |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
# |> filter(fn: (r) => r["_measurement"] == "A" or r["_field"] == "Bat_A" or r["device"] == "mppt-1210-hus")
# |> filter(fn: (r) => r["_measurement"] == "V" or r["_field"] == "Bat_V" or r["device"] == "mppt-1210-hus")
# |> drop(columns: ["_stop"])
# |> drop(columns: ["_start"])
# |> group(columns: ["_time"])
# |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
# |> map(fn: (r) => ({ _time: r._time, "1": r.first, "2": r.second, "3": r.third, "4": r.fourth}))
# |> rename(columns: { "1": "First", "2": "Second", "3": "Third", "4": "Fourth" })
# 
# 

#data_1 = from(bucket:"LabjackCurrentVoltage")
#  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
#  |> filter(fn: (r) => r["_measurement"] == "A" and r["_field"] == "Bat_A" and r["device"] == "mppt-1210-hus")
#  
#data_2 = from(bucket:"LabjackCurrentVoltage")
#  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
#  |> filter(fn: (r) => r["_measurement"] == "V" and r["_field"] == "Bat_V" and r["device"] == "mppt-1210-hus")
#  
#join(
#  tables: {d1: data_1, d2: data_2},
#  |> columns(column: "_value")
#  on: ["_time"]
#)



