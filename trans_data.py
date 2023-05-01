import os
import time
import numpy as np
import Adafruit_ADS1x15

from scipy import signal
from influxdb import InfluxDBClient as influxdb

# influxDB Setting
# IP, Port, ID, PW, DB Name
inf_db = influxdb.InfluxDBClient(IP, 8086, 'mid', 'mid', 'useful')

# ADC 1115 Object Generate
adc = Adafruit_ADS1x15.ADS1115()

# Gain Setting 
GAIN = 2/3

# Action List
mode = ["Left","Center","Right"]

# Count of Repeat
repeat_cnt = 0
mode_cnt = 0

# 1개 기준 1sec = 425
# 한 번에 찍을 값의 개수
timing = 125

# 채널 개수
channel = 1

# 채널 리스트 
channel_list = [x for x in range(channel)]

while True:
    print("1. Sending Wave Values \
    \n2. quit()")
    print("Now, "+mode[mode_cnt])
    menu = int(input())
    
    now_mode = mode[mode_cnt]
    if menu == 1:
        repeat_cnt=0
        for _ in range(1):
            repeat_cnt += 1
            cnt = 0
            # start 
            Start = time.time()
            
            # 2차원 배열 만듦
            for i in range(timing):
                for j in range(channel):
                    {
                        'measurement': '',
                        'tags': {
                            'tag1': 'value1',
                        },
                        'fields': {
                            'field1': 1,
                            'field2': 2
                        }
                    }
                    inf_db.write_points(adc.read_adc(j,gain=GAIN,data_rate = 860))
            
            # end        
            End = time.time()       
            
            Processing_Time = End - Start
            print("Processing Time :",Processing_Time)
    elif menu ==2:
        print("Bye")
        break
           