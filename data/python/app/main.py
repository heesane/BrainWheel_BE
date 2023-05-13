
# Describe Table
# +--------------------+--------------+------+-----+---------+----------------+
# | Field              | Type         | Null | Key | Default | Extra          |
# +--------------------+--------------+------+-----+---------+----------------+
# | id                 | int          | NO   | PRI | NULL    | auto_increment |
# | created_at         | datetime     | NO   |     | NULL    |                |
# | username           | varchar(255) | NO   |     | NULL    |                |
# | password           | varchar(255) | NO   |     | NULL    |                |
# | result             | int(1)       | NO   |     | 0       |                |
# | target_accurate    | int(1)       | NO   |     | 80      |                |
# | flag               | int(1)       | NO   |     | 0       |                |
# | activation         | boolean      | NO   |     | False   |                |
# +--------------------+--------------+------+-----+---------+----------------+

from typing import Optional
from fastapi import FastAPI
from fastapi.responses import FileResponse
from influxdb import client as influxdb
import pymysql
from pydantic import BaseModel
import tool

# SFTP Protocol Server -> Raspberry PI
from tool.send import sftp_upload

# Make Training Model
from tool.LearnFromCsv import train_model

IP = "3.216.219.9"
def login_mysql():
    conn = pymysql.connect(host = IP,
                     port=3306,
                     user='admin',
                     passwd='admin',
                     db='userinfo',
                     charset='utf8',
                     autocommit=True)

    return conn
# Example
# cursor.excute("SHOW TABLES;")
# print(cursor.fetchone())
# cursor.close()
# 입력값 정의
class UserInfo(BaseModel):
    username: str = None
    password: str = None
    target_accurate: int = None

    
app = FastAPI()

inf_db = influxdb.InfluxDBClient(IP,8086,'admin','admin','data')
users = []

# mainpage
@app.get("/")
async def mainpage():
    return "BrainWheel Backend API Server"

###########################################################
###################사용자 관련 API##########################
# 모든 사용자 조회 API
@app.get("/users")
async def get_all_users():
    conn = login_mysql()
    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 실행
            sql = "SELECT * FROM users"
            cursor.execute(sql)

            # 결과 가져오기
            result = cursor.fetchall()
            if result:
                return result
            else:
                {"message":"Not Found User Data"}
            return result
    except Exception as e:
        return {"error": str(e)}

# 사용자 생성 함수
@app.post("/users")
async def create_user(user:UserInfo):
    conn = login_mysql()
    cursor = conn.cursor()
    insert_query = "INSERT INTO users (username, password, target_accurate) VALUES (%s, %s, %s,)"
    cursor.execute(insert_query, (user.username, user.password, user.target_accurate))
    conn.commit()
    conn.close()
    
    inf_query = """CREATE USER %s WITH PASSWORD '%s';
    GRANT ALL ON "users" TO %s;""" % (user.username, user.password)
    inf_db.create_measurement(user.username)
    inf_db.query(inf_query)
    
    return {"message": "UserInfo created successfully"}

# 사용자 조회 함수
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    conn = login_mysql()
    cursor = conn.cursor()
    select_query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(select_query, user_id)
    result = cursor.fetchone()
    conn.close()
    if result:
        user = {
            "id": result[0],
            "username": result[1],
            "password": result[2],
            "target_accurate": result[3],
            
        }
        return user
    else:
        return {"message": "UserInfo not found"}

# 사용자 업데이트 함수
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserInfo):
    conn = login_mysql()
    cursor = conn.cursor()
    update_query = "UPDATE users SET "
    update_values = []
    if user.username is not None:
        update_query += "username = %s, "
        update_values.append(user.username)
    if user.password is not None:
        update_query += "password = %s, "
        update_values.append(user.password)
    if user.target_accurate is not None:
        update_query += "target_accurate = %d, "
        update_values.append(user.target_accurate)
    
    update_query = update_query[:-2] + " WHERE id = %s"
    update_values.append(user_id)
    cursor.execute(update_query, update_values)
    conn.commit()
    conn.close()
    return {"message": "UserInfo updated successfully"}

# 사용자 삭제 함수
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    conn = login_mysql()
    cursor = conn.cursor()
    delete_query = "DELETE FROM users WHERE id = %s"
    cursor.execute(delete_query, user_id)
    conn.commit()
    conn.close()
    return {"message": "UserInfo deleted successfully"}

###########################################################
######################데이터 관련 API#######################
# Flag 수신 처리 함수
@app.get("/flag/{user_name}")
async def ReceiveFlag(user_name: int, flag: str):
    # Flag: inf_success -> csv_success -> h5_success
    if flag == "inf_success":
        while tool.MakeCsv.export_to_csv(IP, 'userinfo', 'admin', 'admin', user_name, 425) != True:
            continue
        csv_flag =True
        return {"flag": "Make CSV Success"}
    
    elif flag == "csv_success":
        while tool.LearnFromCsv.train_model(user_name) != True:
            continue
        h5_flag = True
        return {"flag": "Make H5 Success"}
        
# h5 파일 다운로드 함수
@app.get("/download/{user_id}")
async def download_h5(user_id: str):
    file_path = "h5_file/" + str(user_id) + ".h5"
    return FileResponse(file_path, media_type='application/hdf5', filename=str(user_id) + ".h5")

# 성공 여부 저장
@app.post("/end/{user_name}/success")
async def end_success(user_name: str):
    conn = login_mysql()
    cur = conn.cursor()
    sql = """UPDATE `userinfo`.`users` SET `flag` = '1', `activation` = `True` WHERE (`username` = %s);"""
    conn.execute(sql, user_name)
    conn.commit()
    conn.close()
    
# 정확도 측정 결과
@app.post("/end/{user_name}/{result}")
async def end_result(user_name: str, result: int):
    conn = login_mysql()
    cur = conn.cursor()
    sql = """UPDATE `userinfo`.`users` SET `result` = %d WHERE (`username` = %s);"""
    conn.execute(sql, result, user_name)
    conn.commit()
    conn.close()