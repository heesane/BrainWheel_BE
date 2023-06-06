import os
import pandas as pd
import numpy as np
import csv
import pymysql

from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from influxdb import client as influxdb

from . import config
from . import manage

IP = config.IP

SERVER_PORT = config.SERVER_PORT
MYSQL_PORT = config.MYSQL_PORT
INF_PORT = config.INF_PORT

MYSQL_ADMIN_ID = config.MYSQL_ADMIN_ID
MYSQL_ADMIN_PW = config.MYSQL_ADMIN_PW
INF_ADMIN_ID = config.INF_ADMIN_ID
INF_ADMIN_PW = config.INF_ADMIN_PW

MYSQL_DB_NAME = config.MYSQL_DB_NAME
MYSQL_TABLE_NAME = config.MYSQL_TABLE_NAME
INF_DB_NAME = config.INF_DB_NAME
INF_MEASUREMENT = config.INF_MEASUREMENT

inf_db = influxdb.InfluxDBClient(IP,INF_PORT,INF_ADMIN_ID,INF_ADMIN_PW,INF_DB_NAME)

def login_custom_mysql(user:str,passwd:str,db:str):
    conn = pymysql.connect(host = IP,
                        port=MYSQL_PORT,
                        user=user,
                        passwd=passwd,
                        db=db,
                        charset='utf8',
                        autocommit=True)
    return conn



def login_admin_mysql():
    conn = pymysql.connect(host = IP,
                     port=MYSQL_PORT,
                     user=MYSQL_ADMIN_ID,
                     passwd=MYSQL_ADMIN_PW,
                     db=MYSQL_DB_NAME,
                     charset='utf8',
                     autocommit=True)
    return conn

def login_user_mysql(name:str, pw:str):
    conn = pymysql.connect(host = IP,
                     port=MYSQL_PORT,
                     user=name,
                     passwd=pw,
                     db=MYSQL_DB_NAME,
                     charset='utf8',
                     autocommit=True)
    return conn

def training(plus_csv_file_name, minus_csv_file_name, model_weights_file_name):
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
        
def make_csv(user_name:str, max_data_count:int =425):
    try:

        # InfluxDB에서 데이터 가져오기 (최대 갯수 설정)
        result = inf_db.query('SELECT * FROM %s GROUP BY %s LIMIT %s' % INF_MEASUREMENT,user_name,max_data_count)

        # 결과를 CSV 파일에 저장
        with open(user_name+'.csv', mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(['time','name', 'value'])
            for row in result.get_points():
                writer.writerow([row['time'],row['name'], row['value']])

        # InfluxDB에서 데이터 삭제
        inf_db.query('DELETE FROM %s GROUP BY %s LIMIT %s' % INF_MEASUREMENT,user_name,max_data_count)
        return True
    except influxdb.exceptions.InfluxDBClientError:
        return False
    except IOError:
        return False