import influxdb
import csv

# InfluxDB 연결 설정
inf_db = influxdb.InfluxDBClient(IP, 8086, 'mid', 'mid', 'useful')



# CSV 파일에 저장할 데이터의 최대 갯수 설정
max_data_count = 125
# InfluxDB에서 사용할 DB 이름 설정
name = 'hhs'

# InfluxDB에서 데이터 가져오기 (최대 갯수 설정)
result = inf_db.query('SELECT * FROM %s LIMIT %s' % name,max_data_count)

# 결과를 CSV 파일에 저장
with open('data.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['time','name', 'value'])
    for row in result.get_points():
        writer.writerow([row['time'],row['name'], row['value']])

# InfluxDB에서 데이터 삭제
inf_db.query('DELETE FROM %s LIMIT %s' % name,max_data_count)
