#This Script 
  # 1.gets the measurement data from influxdb
  # 1.1. struct it as follows row1: batteryMilliAmps,	batteryMilliWatts,	isBatteryInFloat,
  #      batteryVoltage,	samplePeriodMilliSec,	timestamp, therest
  # 1.2. writes it to /data/raw_sensor_data.csv
  # 2.Executes ./backtest
  # 3.Reads the calculated SOC from the /data/processed_sensor_data.csv and
  #   writes it back to enhanced_processed_sensor_data.csv
  # 4.Visualise the difference between SOC from Libre Solar Algo and Kalman-SoC Algo.
  # 5.TODO Writes it into the influxdb on the correct place.
 

#requirements: pip3 install influxdb 
import os 
import argparse
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client .client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

bucket ="LabjackCurrentVoltage"
org ="LibreSolar"
token =os.getenv('TOKEN')  # can be set in command line as well if no .env file is used in rootdir
url="https://influxdb.lsserver.uber.space"
toMilli = 1000
currentWorkingDir =  os.getcwd()
outputDataDir = currentWorkingDir + '/data/'
buildDir = currentWorkingDir + '/build/'


def queryDfFromInfluxDb(queryStart,queryStop):

  client = InfluxDBClient(
    url=url,
    token=token,
    org=org
  )

  query_api = client.query_api()
  query = 'from(bucket:"LabjackCurrentVoltage")\
  |> range(start:' + queryStart + ', stop:' + queryStop + ')\
  |> filter(fn: (r) => r["_measurement"] == "V" or r["_measurement"] == "A" or r["_measurement"] == "Info")\
  |> filter(fn: (r) => r["_field"] == "Bat_V" or r["_field"] == "Bat_A" or r["_field"] == "ChgState" or r["_field"] == "SOC_pct")\
  |> filter(fn: (r) => r["device"] == "mppt-1210-hus")'
  # do structing with flux seems inefficient (>8s)
  #|> group(columns: ["_time"])'
  #|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'

  dfQuery = client.query_api().query_data_frame(org=org, query=query)
  dfQuery.to_csv(outputDataDir + queryStart + queryStop + '_dbquery_raw_sensor_data.csv',index=False)
  # csv_result = query_api.query_csv(query,dialect=Dialect(header=False, delimiter=",",
  # comment_prefix="#", annotations=[],date_time_format="RFC3339"))

  #write_api = client.write_api(write_options=SYNCHRONOUS)

  #p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
  #write_api.write(bucket=bucket, org=org, record=p)

  client.close()

def structDataFrameQuery(queryStart,queryStop):

  dfQuery = pd.read_csv(outputDataDir + queryStart + queryStop + '_dbquery_raw_sensor_data.csv')
  dfRawSensorData = dfQuery.pivot(index = '_time',columns = '_field', values='_value').reset_index()
  print(dfRawSensorData)

  dfRawSensorData = dfRawSensorData[['Bat_A', 'ChgState','Bat_V','_time','SOC_pct']] # reorder column to:
  #batteryMilliAmps,	batteryMilliWatts,	isBatteryInFloat,	 batteryVoltage,	samplePeriodMilliSec	 timestamp
  dfRawSensorData["Bat_A"] = dfRawSensorData["Bat_A"] * toMilli
  dfRawSensorData["Bat_V"] = dfRawSensorData["Bat_V"] * toMilli
  dfRawSensorData.insert(1, "batteryMilliWatts",dfRawSensorData['Bat_A'] * dfRawSensorData['Bat_V'] / 1000, True)
  dfRawSensorData.insert(4, "samplePeriodMilliSec", '1000' , True)
  dfRawSensorData = dfRawSensorData.rename(columns={"Bat_A": "batteryMilliAmps", "batteryMilliWatts": "batteryMilliWatts","ChgState": "isBatteryInFloat", "Bat_V": "batteryVoltage", "samplePeriodMilliSec" : "samplePeriodMilliSec", "_time": "timestamp"})
  dfRawSensorData = dfRawSensorData.astype({'batteryMilliAmps' : 'int32',	'batteryMilliWatts' : 'int32','isBatteryInFloat': 'int32',	 'batteryVoltage': 'int32',	'samplePeriodMilliSec': 'int32'})
  print(dfRawSensorData)
  print(dfRawSensorData.info())

  dfRawSensorData.to_csv(outputDataDir + queryStart + queryStop + '_raw_sensor_data.csv',index=False)
  dfRawSensorData.to_csv(outputDataDir + 'raw_sensor_data.csv',index=False)
  
def runCppBacktest():
  subprocess.run("./backtest",cwd = buildDir)


def visualiseProcessedSensorData(queryStart,queryStop):

  dfProcessedSensorData = pd.read_csv(outputDataDir + 'processed_sensor_data.csv')
  dfRawSensorData = pd.read_csv(outputDataDir + 'raw_sensor_data.csv')
  
  dfProcessedSensorDataEnhanced = dfProcessedSensorData
  dfProcessedSensorDataEnhanced.insert(6, "SoC_LibreSolar", dfRawSensorData['SOC_pct']/10, True)
  dfProcessedSensorDataEnhanced["kalman_soc"] =  dfProcessedSensorDataEnhanced["kalman_soc"] / 10000 
  dfProcessedSensorDataEnhanced["batteryMilliWatts"] =  dfProcessedSensorDataEnhanced["batteryMilliWatts"] / 100000 
  dfProcessedSensorDataEnhanced["batteryVoltage"] =  dfProcessedSensorDataEnhanced["batteryVoltage"] / 1000 
  dfProcessedSensorDataEnhanced["batteryMilliAmps"] =  dfProcessedSensorDataEnhanced["batteryMilliAmps"] / 1000 
  dfProcessedSensorDataEnhanced["samplePeriodMilliSec"] =  dfProcessedSensorDataEnhanced["samplePeriodMilliSec"] / 1000 

  dfProcessedSensorDataEnhanced.to_csv(outputDataDir + queryStart + queryStop + '_enhanced_processed_sensor_data.csv',index=False)
  
  #Matplotlib
  #dfProcessedSensorDataEnhanced.plot()
  #plt.show()

  #Plotly
  pd.options.plotting.backend = "plotly"
  fig = dfProcessedSensorDataEnhanced.plot()
  fig.show()


def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("--start", dest="queryStart", help = "Query start at either in -97d or in 2021-05-28T20:10:00.000Z(default)  format", default = "2021-05-28T20:10:00.000Z")
  parser.add_argument("--stop" , dest="queryStop", help =  "Query stops at either in -95d or in 2021-05-29T02:19:00.000Z(default)  format", default = "2021-05-29T01:19:00.000Z")
  args = parser.parse_args()
  queryStart = args.queryStart
  queryStop  = args.queryStop
  existInfluxDbDataQueryFile = os.path.isfile(outputDataDir + queryStart + queryStop + '_dbquery_raw_sensor_data.csv')
  if not existInfluxDbDataQueryFile:
    queryDfFromInfluxDb(queryStart,queryStop)
  
  structDataFrameQuery(queryStart,queryStop)
  runCppBacktest()
  visualiseProcessedSensorData(queryStart,queryStop)

if __name__ == "__main__":
    main()
