from influxdb import InfluxDBClient as influxdb

# InfluxDB 연결 설정
inf_db = influxdb.InfluxDBClient(IP, 8086, 'mid', 'mid', 'useful')

# InfluxDB에 보낼 데이터 설정
data = [
    {
        'measurement': 'my_measurement',
        'tags': {
            'tag1': 'value1',
            'tag2': 'value2'
        },
        'fields': {
            'field1': 1,
            'field2': 2
        }
    },
    {
        'measurement': 'my_measurement',
        'tags': {
            'tag1': 'value1',
            'tag2': 'value2'
        },
        'fields': {
            'field1': 3,
            'field2': 4
        }
    },
    # ...
]

# InfluxDB에 보낼 최대 데이터 갯수 설정
max_data_count = 1000

# 최대 데이터 갯수까지 데이터를 InfluxDB에 보냄
for i in range(0, len(data), max_data_count):
    inf_db.write_points(data[i:i+max_data_count])
