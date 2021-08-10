#This Script 
  # 1.gets the measurement data from influxdb, struct it and write to /data/raw_sensor_data.csv
  # 2.Executes ./backtest
  # 3.Reads the calculated SOC from the /data/processed_sensor_data.csv
  # 4.Writes it into the influxdb on the correct place. 
  
#requirements: python3 -m pip install influxdb ? 

import subprocess
import requests
from influxdb_client import InfluxDBClient, Point, Dialect



bucket ="LabjackCurrentVoltage"
org ="LibreSolar"
token ="environement-variable"
url="https://influxdb.lsserver.uber.space"

client = InfluxDBClient(
   url=url,
   token=token,
   org=org
)

#write_api = client.write_api(write_options=SYNCHRONOUS)

#p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
#write_api.write(bucket=bucket, org=org, record=p)


query_api = client.query_api()
query = 'from(bucket:"LabjackCurrentVoltage")\
|> range(start: -97d, stop: -96d)\
|> filter(fn: (r) => r["_measurement"] == "V" or r["_measurement"] == "A" or r["_measurement"] == "Info")\
|> filter(fn: (r) => r["_field"] == "Bat_V" or r["_field"] == "Bat_A" or r["_field"] == "ChgState" or r["_field"] == "SOC_pct")\
|> filter(fn: (r) => r["device"] == "mppt-1210-hus")'

"""
Query: using csv library
"""
csv_result = query_api.query_csv(query,dialect=Dialect(header=False, delimiter=",", comment_prefix="#", annotations=[],date_time_format="RFC3339"))
for csv_line in csv_result:
    if not len(csv_line) == 0:
        print(f'Temperature in {csv_line[9]} is {csv_line[6]}')

"""
Close client
"""
client.close()

#subprocess.run(["./backtest"])

