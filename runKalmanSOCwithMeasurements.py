#This Script 
  # 1.gets the measurement data from influxdb
  # 1.1. struct it as follows row1: batteryMilliAmps,	batteryMilliWatts,	isBatteryInFloat,
  #      batteryVoltage,	samplePeriodMilliSec,	timestamp, therest
  # 1.2. write to /data/raw_sensor_data.csv
  # 2.Executes ./backtest
  # 3.Reads the calculated SOC from the /data/processed_sensor_data.csv
  # 4.Visualise the difference between SOC from Libre Solar Algo and Kalman-SoC Algo.
  # 5.Writes it into the influxdb on the correct place.
 

#requirements: python3 -m pip install influxdb ?
import os 
import subprocess
import pandas as pd
from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client .client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

bucket ="LabjackCurrentVoltage"
org ="LibreSolar"
token =os.getenv('TOKEN')  # can be set in command line as well if no .env file is used in rootdir
url="https://influxdb.lsserver.uber.space"
toMilli = 1000
queryStart = '2021-05-28T20:10:00.000Z'
queryStop = '2021-05-29T02:19:00.000Z'
currentWorkingDir =  os.getcwd()
outputDataDir = currentWorkingDir + '/data/'
buildDir = currentWorkingDir + '/build/'

if not (os.path.isfile(outputDataDir + queryStart + queryStop + '_nonstruct_raw_sensor_data.csv')):
  print(outputDataDir + queryStart + queryStop + '_nonstruct_raw_sensor_data_.csv')
  client = InfluxDBClient(
    url=url,
    token=token,
    org=org
  )
  # |> range(start: -97d, stop: -95d)
  query_api = client.query_api()
  query = 'from(bucket:"LabjackCurrentVoltage")\
  |> range(start:' + queryStart + ', stop:' + queryStop + ')\
  |> filter(fn: (r) => r["_measurement"] == "V" or r["_measurement"] == "A" or r["_measurement"] == "Info")\
  |> filter(fn: (r) => r["_field"] == "Bat_V" or r["_field"] == "Bat_A" or r["_field"] == "ChgState" or r["_field"] == "SOC_pct")\
  |> filter(fn: (r) => r["device"] == "mppt-1210-hus")'
  # do structing with flux seems inefficient (>8s)
  #|> group(columns: ["_time"])'
  #|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'


  # csv_result = query_api.query_csv(query,dialect=Dialect(header=False, delimiter=",",
  # comment_prefix="#", annotations=[],date_time_format="RFC3339"))

  dfQuery= client.query_api().query_data_frame(org=org, query=query)
  dfQuery.to_csv(outputDataDir + queryStart + queryStop + '_nonstruct_raw_sensor_data.csv',index=False)

  client.close()

else: dfQuery = pd.read_csv(outputDataDir + queryStart + queryStop + '_nonstruct_raw_sensor_data.csv')

print(dfQuery)

dfRawSensorData = dfQuery.pivot(index = '_time',columns = '_field', values='_value').reset_index()
print(dfRawSensorData)

dfRawSensorData = dfRawSensorData[['Bat_A', 'ChgState','Bat_V','_time','SOC_pct']] # reorder column to:
#batteryMilliAmps,	batteryMilliWatts,	isBatteryInFloat,	 batteryVoltage,	samplePeriodMilliSec	 timestamp
dfRawSensorData["Bat_A"] = toMilli * dfRawSensorData["Bat_A"]
dfRawSensorData["Bat_V"] = toMilli * dfRawSensorData["Bat_V"]
dfRawSensorData.insert(1, "batteryMilliWatts",dfRawSensorData['Bat_A'] * dfRawSensorData['Bat_V'] , True)
dfRawSensorData.insert(4, "samplePeriodMilliSec", '1' , True)
dfRawSensorData = dfRawSensorData.rename(columns={"Bat_A": "batteryMilliAmps", "batteryMilliWatts": "batteryMilliWatts","ChgState": "isBatteryInFloat", "Bat_V": "batteryVoltage", "samplePeriodMilliSec" : "samplePeriodMilliSec", "_time": "timestamp"})
dfRawSensorData = dfRawSensorData.astype({'batteryMilliAmps' : 'int32',	'batteryMilliWatts' : 'int32','isBatteryInFloat': 'int32',	 'batteryVoltage': 'int32',	'samplePeriodMilliSec': 'int32'})
print(dfRawSensorData)
print(dfRawSensorData.info())

dfRawSensorData.to_csv(outputDataDir + queryStart + queryStop + '_raw_sensor_data.csv',index=False)
dfRawSensorData.to_csv(outputDataDir + 'raw_sensor_data.csv',index=False)

subprocess.run("./backtest",cwd = buildDir)

dfProcessedSensorData = pd.read_csv(outputDataDir + 'processed_sensor_data.csv')
dfRawSensorData.to_csv(outputDataDir + queryStart + queryStop + '_processed_sensor_data.csv',index=False)
#dfProcessedSensorDataEnhanced = dfProcessedSensorData.insert()
 

#write_api = client.write_api(write_options=SYNCHRONOUS)

#p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
#write_api.write(bucket=bucket, org=org, record=p)


