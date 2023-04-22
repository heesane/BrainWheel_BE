# 1. 뇌파 측정기로 데이터를 읽음
# 2. 해당 데이터를 influxdb로 보냄
# 3. user별로 새로운 table 생성 -> DB에 어느정도의 부하?
# 4. 서버에서 인공지능 프로그램 실행
# Describe Table
# +--------------+--------------+------+-----+---------+----------------+
# | Field        | Type         | Null | Key | Default | Extra          |
# +--------------+--------------+------+-----+---------+----------------+
# | id           | int          | NO   | PRI | NULL    | auto_increment |
# | username     | varchar(255) | NO   |     | NULL    |                |
# | password     | varchar(255) | NO   |     | NULL    |                |
# | Is_active    | tinyint(1)   | NO   |     | 1       |                |
# | phone_number | varchar(255) | NO   |     | NULL    |                |
# +--------------+--------------+------+-----+---------+----------------+

# 04.21수정 사항 CRUD 구현

from typing import Optional
from fastapi import FastAPI
from influxdb import client as influxdb
import pymysql
from pydantic import BaseModel

# SFTP Protocol Loacl -> Raspberry PI
from learn_transmit.transmit import sftp_upload
# Make Training Model
from learn_transmit.learn import train_model

IP = "3.216.219.9"
def login_mysql():
    conn = pymysql.connect(host = IP,
                     port=3306,
                     user='hhs',
                     passwd='5499458kK@',
                     db='test_db',
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
    is_active: int = None
    phone_number: str = None
    
    
app = FastAPI()

# inf_db = influxdb.InfluxDBClient(IP,8086,'mid','mid','useful')
users = []

# mainpage
@app.get("/")
async def mainpage():
    return "Hello"

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
def create_user(user:UserInfo):
    conn = login_mysql()
    cursor = conn.cursor()
    insert_query = "INSERT INTO users (username, password, is_active, phone_number) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (user.username, user.password, user.is_active, user.phone_number))
    conn.commit()
    conn.close()
    return {"message": "UserInfo created successfully"}

# 사용자 조회 함수
@app.get("/users/{user_id}")
def get_user(user_id: int):
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
            "is_active": result[3],
            "phone_number": result[4]
        }
        return user
    else:
        return {"message": "UserInfo not found"}

# 사용자 업데이트 함수
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserInfo):
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
    if user.is_active is not None:
        update_query += "is_active = %s, "
        update_values.append(user.is_active)
    if user.phone_number is not None:
        update_query += "phone_number = %s, "
        update_values.append(user.phone_number)
    update_query = update_query[:-2] + " WHERE id = %s"
    update_values.append(user_id)
    cursor.execute(update_query, update_values)
    conn.commit()
    conn.close()
    return {"message": "UserInfo updated successfully"}

# 사용자 삭제 함수
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = login_mysql()
    cursor = conn.cursor()
    delete_query = "DELETE FROM users WHERE id = %s"
    cursor.execute(delete_query, user_id)
    conn.commit()
    conn.close()
    return {"message": "UserInfo deleted successfully"}

