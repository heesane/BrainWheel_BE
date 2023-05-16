from influxdb import InfluxDBClient as influxdb
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import requests
import csv
import socket
import os
import pandas as pd
import numpy as np

# Raspberry PI Side
def write_to_influxdb(IP, database, username, password, data, max_data_count=425):
    """\
    InfluxDB에 데이터를 저장하는 함수
    param IP: InfluxDB IP 주소
    """
    inf_db = influxdb(IP, 8086, username, password, database)
    try:
        for i in range(0, len(data), max_data_count):
            inf_db.write_points(data[i:i+max_data_count])
    except influxdb.exceptions.InfluxDBClientError:
        print("연결 에러")
        
# Raspberry PI Side
def SendFlag(IP: str,PORT:int):
    """\
    Args:
        IP (String): Server IP\n
        PORT (String): Server PORT
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP, PORT))
        s.sendall("1".encode())
        s.close()
    except socket.error:
        print("연결 에러")
    
        
def export_to_csv(IP, database, username, password, measurement, max_data_count=1000):
    try:
        # InfluxDB 연결 설정
        inf_db = influxdb.InfluxDBClient(IP, 8086, username, password, database)

        # InfluxDB에서 데이터 가져오기 (최대 갯수 설정)
        result = inf_db.query('SELECT * FROM %s LIMIT %s' % measurement,max_data_count)

        # 결과를 CSV 파일에 저장
        with open(username+'.csv', mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(['time','name', 'value'])
            for row in result.get_points():
                writer.writerow([row['time'],row['name'], row['value']])

        # InfluxDB에서 데이터 삭제
        inf_db.query('DELETE FROM %s LIMIT %s' % measurement,max_data_count)
    except influxdb.exceptions.InfluxDBClientError:
        print("연결 에러")
    except IOError:
        print("저장 에러")
    
# def get_local_ip_address():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(("8.8.8.8", 80))
#         local_ip = s.getsockname()[0]
#         s.close()
        
#     except socket.error:
#         local_ip = None
        
#     return local_ip

