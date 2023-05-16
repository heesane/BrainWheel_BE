from influxdb import InfluxDBClient as influxdb


def write_to_influxdb(IP, database, username, password, data, max_data_count=1000):
    """
    InfluxDB에 데이터를 저장하는 함수
    """
    try:
        inf_db = influxdb(IP, 8086, username, password, database)

        for i in range(0, len(data), max_data_count):
            inf_db.write_points(data[i:i+max_data_count])
    except influxdb.exceptions.InfluxDBClientError:
        print("연결 에러")