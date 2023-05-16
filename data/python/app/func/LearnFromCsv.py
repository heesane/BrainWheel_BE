# SIDE:Server
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import pandas as pd
import numpy as np

"""
기능 정리
1. csv_folder에 있는 csv파일을 기반으로 학습
2. h5_file folder가 없으면 자동으로 생성하고 .h5파일을 저장

호출방법
from learn_transmit.learn import train_model
train_model("plus.csv","minus.csv","test_generated.h5")
"""

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
