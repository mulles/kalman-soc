#This Script 
  # 1.gets the measurement data from influxdb or VictoriaMetricsQueryFile
  # 1.1. struct it as follows row1: batteryMilliAmps,	batteryMilliWatts,	isBatteryInFloat,
  #      batteryVoltage,	samplePeriodMilliSec,	timestamp, therest
  # 1.2. writes it to /data/raw_sensor_data.csv
  # 2.Executes ./backtest
  # 3.Reads the calculated SOC from the /data/processed_sensor_data.csv and
  #   writes it back to *enhanced_processed_sensor_data.csv
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
buildFolderName = '/build/'
buildDir = currentWorkingDir + buildFolderName


def queryDfFromInfluxDb(device,queryStart,queryStop):
  print(outputDataDir + device  + '_' +  queryStart + queryStop + '_dbquery_raw_sensor_data.zip')
  if not os.path.exists(outputDataDir + device  + '_' +  queryStart + queryStop + '_dbquery_raw_sensor_data.zip') : 
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
      dfQuery.to_csv(device  + '_' + outputDataDir + queryStart + queryStop + '_dbquery_raw_sensor_data.zip',index=False,compression={'method':'zip','archive_name': outputDataDir +  device  + '_' + queryStart + queryStop + '_dbquery_raw_sensor_data.csv'})

      client.close()

def structDataFrameInfluxDbQuery(device,queryStart,queryStop):

  dfQuery = pd.read_csv(outputDataDir + device  + '_'  + queryStart + queryStop + '_dbquery_raw_sensor_data.zip')
  dfRawSensorData = dfQuery.pivot(index = '_time',columns = '_field', values='_value').reset_index()
  dfRawSensorData = dfRawSensorData[['Bat_A', 'ChgState','Bat_V','_time','SOC_pct']] # reorder column to:
  #batteryMilliAmps,	batteryMilliWatts,	isBatteryInFloat,	 batteryVoltage,	samplePeriodMilliSec	 timestamp
  dfRawSensorData["Bat_A"] = dfRawSensorData["Bat_A"] * toMilli
  dfRawSensorData["Bat_V"] = dfRawSensorData["Bat_V"] * toMilli
  dfRawSensorData.insert(1, "batteryMilliWatts",dfRawSensorData['Bat_A'] * dfRawSensorData['Bat_V'] / 1000, True)
  dfRawSensorData.insert(4, "samplePeriodMilliSec", '1000' , True)
  dfRawSensorData = dfRawSensorData.rename(columns={"Bat_A": "batteryMilliAmps", "batteryMilliWatts": "batteryMilliWatts","ChgState": "isBatteryInFloat", "Bat_V": "batteryVoltage", "samplePeriodMilliSec" : "samplePeriodMilliSec", "_time": "timestamp"})
  dfRawSensorData = dfRawSensorData.astype({'batteryMilliAmps' : 'int32',	'batteryMilliWatts' : 'int32','isBatteryInFloat': 'int32',	 'batteryVoltage': 'int32',	'samplePeriodMilliSec': 'int32'})

  dfRawSensorData.to_csv(outputDataDir + device  + '_' + queryStart + queryStop + '_raw_sensor_data.zip',index=False,compression={'method':'zip','archive_name': outputDataDir + device  + '_' +  queryStart + queryStop + '_raw_sensor_data.csv'})
  dfRawSensorData.to_csv(outputDataDir + 'raw_sensor_data.csv',index=False)


def structDataFrameVictoriaMQuery(device,queryStart,queryStop):
  
  dfQuery = pd.read_csv(outputDataDir + device  + '_' + queryStart + '-' + queryStop + '.zip')
  dfRawSensorData = dfQuery[['ChgState','Bat_V','Time_s','SOC_pct','Load_W','Solar_W','Grid_W']].copy() # reorder column to:
  #batteryMilliAmps,	batteryMilliWatts,	isBatteryInFloat,	 batteryVoltage,	samplePeriodMilliSec	 timestamp
  #dfRawSensorData["Bat_A"] = dfRawSensorData["Bat_A"] * toMilli
  dfRawSensorData.loc[:, "Bat_V"] = dfRawSensorData["Bat_V"] * toMilli
  dfRawSensorData.insert(0, "batteryMilliWatts",-( dfRawSensorData['Load_W'] + dfRawSensorData['Grid_W'] + dfRawSensorData['Solar_W'])*toMilli, True)
  dfRawSensorData.insert(1, "Bat_A", dfRawSensorData["batteryMilliWatts"] / dfRawSensorData["Bat_V"] *1000 , True)
  dfRawSensorData.insert(4, "samplePeriodMilliSec", '300000' , True)
  dfRawSensorData = dfRawSensorData.rename(columns={"Bat_A": "batteryMilliAmps", "batteryMilliWatts": "batteryMilliWatts","ChgState": "isBatteryInFloat", "Bat_V": "batteryVoltage", "samplePeriodMilliSec" : "samplePeriodMilliSec", "Time_s": "timestamp"})
  dfRawSensorData = dfRawSensorData.astype({'batteryMilliAmps' : 'int32',	'batteryMilliWatts' : 'int32','isBatteryInFloat': 'int32',	 'batteryVoltage': 'int32',	'samplePeriodMilliSec': 'int32'})

  dfRawSensorData.to_csv(outputDataDir + device + '_raw_sensor_data.zip',index=False, compression={'method':'zip','archive_name': outputDataDir + device + '_raw_sensor_data.zip'})
  dfRawSensorData.to_csv(outputDataDir + 'raw_sensor_data.csv',index=False)

  
def runCppBacktest():
  subprocess.run("./backtest",cwd = buildDir)

def generateBuildFolder():

  if not os.path.exists(buildDir) : 
    subprocess.run("meson setup" + buildFolderName)

def compile(): 
  subprocess.run("ninja", cwd = buildDir)

def runtests(): 
  subprocess.run("./run_tests", cwd = buildDir)


def visualiseProcessedSensorData(device, queryStart,queryStop):

  dfProcessedSensorData = pd.read_csv(outputDataDir + 'processed_sensor_data.csv')
  dfRawSensorData = pd.read_csv(outputDataDir + 'raw_sensor_data.csv')
  
  dfProcessedSensorDataEnhanced = dfProcessedSensorData
  dfProcessedSensorDataEnhanced.insert(6, "SoC_LibreSolar", dfRawSensorData['SOC_pct']/10, True)
  dfProcessedSensorDataEnhanced["kalman_soc"] =  dfProcessedSensorDataEnhanced["kalman_soc"] / 10000 
  dfProcessedSensorDataEnhanced["batteryMilliWatts"] =  dfProcessedSensorDataEnhanced["batteryMilliWatts"] / 100000 
  dfProcessedSensorDataEnhanced["batteryVoltage"] =  dfProcessedSensorDataEnhanced["batteryVoltage"] / 1000 
  dfProcessedSensorDataEnhanced["batteryMilliAmps"] =  dfProcessedSensorDataEnhanced["batteryMilliAmps"] / 1000 
  dfProcessedSensorDataEnhanced["samplePeriodMilliSec"] =  dfProcessedSensorDataEnhanced["samplePeriodMilliSec"] / 1000 /60  # 5 min 
  dfProcessedSensorDataEnhanced = dfProcessedSensorDataEnhanced.rename(columns={"batteryMilliAmps": "Bat_A", "batteryMilliWatts": "Bat_W","isBatteryInFloat": "ChgState", "batteryVoltage": "Bat_V","samplePeriodMilliSec" : "samplePeriodMin"})
  dfProcessedSensorDataEnhanced.to_csv(outputDataDir + device + '_' + queryStart + '-' + queryStop + '_enhanced_processed_sensor_data.zip',index=False,compression={'method':'zip','archive_name': outputDataDir + device + '_' + queryStart + '-' + queryStop + '_enhanced_processed_sensor_data.csv'})
  
  #Matplotlib
  #dfProcessedSensorDataEnhanced.plot()
  #plt.show()

  #Plotly
  pd.options.plotting.backend = "plotly"
  fig = dfProcessedSensorDataEnhanced.plot()
  fig.update_layout(title_text='<b>'+ device + '_' + queryStart + '-' + queryStop + '</b>', title_x=0.5)
  fig.show()
  fig.write_html(outputDataDir + device + '_' + queryStart + '-' + queryStop + '_SOC_Graph.html')

def main():

  
  generateBuildFolder()
  compile()
  runtests()
  
  parser = argparse.ArgumentParser()
  parser.add_argument("--start", dest="queryStart", help = "Query start at either in -97d or in 2021-05-28T20:10:00.000Z(default)  format", default = "2021-05-05T16:11:00.000Z")
  parser.add_argument("--stop" , dest="queryStop", help =  "Query stops at either in -95d or in 2021-05-29T02:19:00.000Z(default)  format", default = "2021-05-29T00:19:00.000Z")
  parser.add_argument("--device" , dest="device", help =  "Device the data has been gathered with", default = "mppt-1210-hus")
  args = parser.parse_args()
  queryStart = args.queryStart
  queryStop  = args.queryStop
  device = args.device
  
  if device == 'mppt-1210-hus': 
  #   queryDfFromInfluxDb(device,queryStart,queryStop)
    structDataFrameInfluxDbQuery(device,queryStart,queryStop)
  # else: 
  #   structDataFrameVictoriaMQuery(device,queryStart,queryStop)

  runCppBacktest()
  visualiseProcessedSensorData(device, queryStart,queryStop)

if __name__ == "__main__":
    main()
