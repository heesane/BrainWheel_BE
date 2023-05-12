#--------------------------------Library-------------------------------#
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

#----------------------------global variable----------------------------#

# Raspberry PI Variable
adc = Adafruit_ADS1x15.ADS1115() # ADC 1115 Object Generate
GAIN = 2/3 # ADC 1115 Gain


# Server Variable
IP = "3.216.219.9"
PORT = "5000"
inf_PORT = 8086
sql_PORT = 3306


# MySQL Variable
## database
mysql_database = "test_db"
## table
mysql_table = "users"

# InfluxDB Variable
## database
inf_database = "data"
## measurement
inf_measurement = "mid"

# Request URL
fixed_url =  f"http://{IP}:{PORT}/"
csv_url = fixed_url + "flag/{user}?flag=csv_success" 
flag_url = fixed_url + "flag/{user}?flag=h5_success"
download_url= fixed_url + "download/{user}"

# Flag
flag = False

#-----------------------------function-----------------------------#

## Input User Info
# Input: None
# Return: user_info (list), user (str), passwd (str), target_accurate (int)
def init():
    
    # User Variable
    user_info = []
    user = ""
    passwd =""
    target_accurate = 0
    
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
                     db='userinfo',
                     charset='utf8',
                     table='users',
                     autocommit=True)
    return conn

## Login InfluxDB
def login_infdb():
    inf_db = influxdb(IP, inf_PORT, my_name, my_password, inf_database)
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
    sql = """INSERT INTO `userinfo`.`users` (`id`, `passwd`, `target_accurate`) VALUES (%s, %s, %d)"""
    try:
        cur.execute(sql, data)
        conn.commit()
        return True
    except:
        conn.rollback()
        return False
    finally:
        conn.close()
        
        
# InfluxDB에 데이터 저장
def write_to_influxdb(username:str,max_data_count:int =425):
    global user
    inf_db = login_infdb()
    data_box = [
        {
            "measurement": username,
            "tags": {
                "name": username
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
        # 실패
        if CsvResponse.status_code != 200:
            print(f"Failed to send GET request for CSV. Response status code: {CsvResponse.status_code}")
            time.sleep(10)
            continue
        # 성공 => flag 값 확인
        json_data = CsvResponse.json()
        csv_value = json_data.get("flag")

        if csv_value != "Make CSV Success":
            print(f"Failed to generate CSV. CSV value: {csv_value}")
            time.sleep(10)
            continue
            
        FlagResponse = requests.get(flag_url)
        if FlagResponse.status_code != 200:
            print(f"Failed to send GET request for flag. Response status code: {FlagResponse.status_code}")
            time.sleep(10)
            continue

        json_data = FlagResponse.json()
        flag_value = json_data.get("flag")

        if flag_value != "MAKE H5 Success":
            print(f"Failed to generate H5. H5 flag value: {flag_value}")
            time.sleep(10)
            continue

        DownloadResponse = requests.get(download_url)
        if DownloadResponse.status_code != 200:
            print(f"Failed to send GET request for downloading H5. Response status code: {DownloadResponse.status_code}")
            time.sleep(10)
            continue
        
        # 경로 자동 생성
        path = "./h5_file"
        if not os.path.isdir(path):
            os.mkdir(path)
            
        with open(f"{path}/{my_name}.h5", "wb") as f:
            f.write(DownloadResponse.content)

        print("Download Success!")
        break
    return True

#-----------------------------main-----------------------------#

while True:
    my_info,my_name,my_password,target_accurate = init()
    
    if SendInfoToSQL(my_info) != True:
        continue

    if write_to_influxdb(my_name) != True:
        print("InfluxDB에 데이터 저장 실패")
        continue
    
    req_data = requests.get(f"http://{IP}:{PORT}/flag/{my_name}?flag=inf_success")
    

    if FlagCheckAndDownload() != True:
        continue
    
    flag = True
        
    model = keras.models.load_model(f"./h5_file/{my_name}.h5")

    while flag == True:
    # h5파일을 불러옴
    
    # 425개의 데이터를 측정
    data = measure(425)
    # 425개의 데이터를 2차원 배열로 변환
    data = np.array(data).reshape(1,-1)
    # 데이터를 표준화
    scaler = StandardScaler()
    scaler.fit(data)
    data = scaler.transform(data)
    # 데이터를 예측
    result = model.predict(data)
    # 예측한 데이터를 0~100사이의 정수로 변환
    result = int(result[0][0]*100)
    # 예측한 데이터를 서버로 전송
    requests.post(f"http://{IP}:{PORT}/result/{my_name}/{result}")
    # 예측한 데이터를 출력
    print(result)
    # 예측한 데이터가 목표치보다 높으면 종료
    if result > target_accurate:
        print("Success!")
        # 서버에 종료를 알림
        requests.post(f"http://{IP}:{PORT}/end/{my_name}/success")
        break
    else:
        print("Failed!")
    # 1초마다 측정
    time.sleep(1)
