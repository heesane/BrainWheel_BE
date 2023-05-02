from influxdb import InfluxDBClient as influxdb
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import csv
import socket
import os
import pandas as pd
import numpy as np


def write_to_influxdb(IP, database, username, password, data, max_data_count=1000):
    """\
    InfluxDB에 데이터를 저장하는 함수
    """
    try:
        inf_db = influxdb(IP, 8086, username, password, database)

        for i in range(0, len(data), max_data_count):
            inf_db.write_points(data[i:i+max_data_count])
    except influxdb.exceptions.InfluxDBClientError:
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
    
def get_local_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
    except socket.error:
        local_ip = None
        
    return local_ip

def train_model(plus_csv_file_name, minus_csv_file_name, model_weights_file_name):
    local_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = local_path + '/csv_folder/'
    
    try:
        pl_csv_path = csv_path + plus_csv_file_name
        mi_csv_path = csv_path + minus_csv_file_name
        
        eye_left_pl = pd.read_csv(pl_csv_path)
        eye_left_mi = pd.read_csv(mi_csv_path)

        left_pl_move = eye_left_pl.iloc[0::3, 1:].values.reshape(-1, 1)
        center_pl_move = eye_left_pl.iloc[1::3, 1:].values.reshape(-1, 1)
        right_pl_move = eye_left_pl.iloc[2::3, 1:].values.reshape(-1, 1)

        move_input = np.concatenate((left_pl_move, center_pl_move, right_pl_move))
        move_target = np.concatenate((np.zeros(1250), np.ones(1250), np.ones(1250) * 2))

        ss = StandardScaler()
        ss.fit(move_input)
        move_input = ss.transform(move_input)

        train_input, train_target = move_input, move_target

        model = keras.Sequential()
        model.add(keras.layers.Flatten(input_shape=(1,)))
        model.add(keras.layers.Dense(30, activation='relu'))
        model.add(keras.layers.Dropout(0.1))
        model.add(keras.layers.Dense(3, activation='softmax'))

        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        save_path = local_path +"/h5_file"
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # whole.h5
        model.save(save_path+"/"+model_weights_file_name)
        
    except Exception as e:
        print(f"Error Name : {e}")
    finally:
        print("Done")
