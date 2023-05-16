from influxdb import client as influxdb
import csv

def make_csv(IP, database, username, password, measurement, max_data_count=1000):
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
        return True
    except influxdb.exceptions.InfluxDBClientError:
        return False
    except IOError:
        return False