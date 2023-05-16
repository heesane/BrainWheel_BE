from influxdb import InfluxDBClient as influxdb
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import requests
import csv
import socket
import os
import time
import pandas as pd
import numpy as np
import pymysql
import Adafruit_ADS1x15
import datetime
flag = False

# Raspberry PI Variable
adc = Adafruit_ADS1x15.ADS1115() # ADC 1115 Object Generate
GAIN = 2/3 # ADC 1115 Gain


# Server Variable
IP = "3.216.219.9"
PORT = "5000"
inf_PORT = 8086
sql_PORT = 3306
# User Variable
user = "hhs"
passwd = "hhs"
target_accurate = 0
user_info=[]
# MySQL Variable
## database
mysql_database = "test_db"
## table
mysql_table = "data"

# InfluxDB Variable
## database
inf_database = "useful"
## measurement
inf_measurement = "mid"

# Request URL
csv_url = f"http://{IP}:{PORT}/csvflag/{user}" 
flag_url = f"http://{IP}:{PORT}/flag/{user}"
download_url= f"http://{IP}:{PORT}/download/{user}"

# Flag
# TODO: Flag를 사용하여 데이터를 전송할지 말지 결정


################# Function #################

## Input User Info
# Input: None
# Return: user_info (list), user (str), passwd (str), target_accurate (int)
def init():
    global user_info,user,passwd,target_accurate
    user_info.append(input("ID: "))
    user_info.append(input("Passwd: "))
    user_info.append(int(input("Target Accurate: ")))
    user = user_info[0]
    passwd = user_info[1]
    target_accurate = user_info[2]
    return user_info,user,passwd,target_accurate

## Login MySQL
def login_mysql():
    global user_info
    conn = pymysql.connect(host = IP,
                     port=sql_PORT,
                     user=user_info[0],
                     passwd=user_info[1],
                     db='test_db',
                     charset='utf8',
                     table='data',
                     autocommit=True)
    return conn

## Login InfluxDB
def login_infdb():
    inf_db = influxdb(IP, inf_PORT, user, passwd, inf_database)
    return inf_db

## BrainWave Data Measure 
# Input: cnt (int)
# Return: Box (list)
def measure(cnt:int):
    box = []
    for i in range(cnt):
        box.append(adc.read_adc(0, gain=GAIN, data_rate=860))
    return box

## Send UserInfo To Server 
# Input: data (list)
def SendInfoToSQL(data:list):
    conn = login_mysql()
    cur = conn.cursor()
    sql = """INSERT INTO `test_db`.`data` (`id`, `passwd`, `target_accurate`) VALUES (%s, %s, %d)"""
    try:
        cur.execute(sql, data)
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()
        
# InfluxDB에 데이터 저장
def write_to_influxdb(max_data_count=425):
    global user
    inf_db = login_infdb()
    data_box = [
        {
            "measurement": user,
            "tags": {
                "name": user
            },
            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                "value": measure(max_data_count)
            }
        }
    ]
    try:
        inf_db.write_points(data_box)
        return True
    except influxdb.exceptions.InfluxDBClientError:
        print("연결 에러")
        return False

# h5파일을 다운받는 함수
def FlagCheckAndDownload():
    while True:
        CsvResponse = requests.get(csv_url)
        if CsvResponse.status_code != 200:
            print(f"Failed to send GET request for CSV. Response status code: {CsvResponse.status_code}")
            continue
        
        json_data = CsvResponse.json()
        csv_value = json_data.get("csv")

        if csv_value != "SuccessGeneratingCSV":
            print(f"Failed to generate CSV. CSV value: {csv_value}")
            continue
            
        FlagResponse = requests.get(flag_url)
        if FlagResponse.status_code != 200:
            print(f"Failed to send GET request for flag. Response status code: {FlagResponse.status_code}")
            continue

        json_data = FlagResponse.json()
        flag_value = json_data.get("flag")

        if flag_value != "SuccessGeneratingH5":
            print(f"Failed to generate H5. H5 flag value: {flag_value}")
            continue

        DownloadResponse = requests.get(download_url)
        if DownloadResponse.status_code != 200:
            print(f"Failed to send GET request for downloading H5. Response status code: {DownloadResponse.status_code}")
            continue

        with open(f"./h5_file/{user}.h5", "wb") as f:
            f.write(DownloadResponse.content)

        print("Download Success!")
        break
    
    
    
