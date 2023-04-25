from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import csv

eye_left_pl = pd.read_csv('plus.csv')
eye_left_mi = pd.read_csv('minus.csv')


left_pl_move = eye_left_pl.to_numpy()[0::3,1:].reshape(-1,1)
center_pl_move = eye_left_pl.to_numpy()[1::3,1:].reshape(-1,1)
right_pl_move = eye_left_pl.to_numpy()[2::3,1:].reshape(-1,1)

move_input = np.concatenate((left_pl_move, center_pl_move, right_pl_move))
move_target = np.concatenate((np.zeros(1250),np.ones(1250),np.ones(1250)*2))

train_input, test_input, train_target, test_target = train_test_split(move_input, move_target, random_state = 42)

ss = StandardScaler()
ss.fit(train_input)
train_input_scaled = ss.transform(train_input)
test_input_scaled = ss.transform(test_input)

# train_input, train_target = move_input, move_target


def model_fn(a_layer=None):
    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape=(1,)))
    model.add(keras.layers.Dense(30,activation='relu'))
    if a_layer:
        model.add(a_layer)
    model.add(keras.layers.Dense(3,activation='softmax'))
    
    return model

model = model_fn(keras.layers.Dropout(0.1))
model.compile(optimizer='adam',loss = 'sparse_categorical_crossentropy',metrics='accuracy')
model.fit(train_input_scaled, train_target, epochs = 30)
model.summary()

# model.save_weights('C:/Users/LG/Desktop/v/model_weights.h5')
model.save('model_whole.h5')