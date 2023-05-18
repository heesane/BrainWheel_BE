# Userinfo.
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
from fastapi import FastAPI,Request,APIRouter
from fastapi.responses import FileResponse
from influxdb import client as influxdb
import pymysql
from pydantic import BaseModel
import os
import datetime


from routers import models
import tool

UserInfo = models.User

router = APIRouter(prefix="/user", tags=["user"])

inf_db = tool.inf_db

# 모든 사용자 조회 API
@router.get("")
async def get_all_users():
    conn = tool.login_admin_mysql()
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

# Admin 
# 사용자 생성 함수
@router.post("")
async def create_user(user:UserInfo):
    conn = tool.login_admin_mysql()
    cursor = conn.cursor()
    
    insert_query = "INSERT INTO users (created_at, username, password, target_accurate) VALUES (%s, %s, %s, %s,)"
    cursor.execute(insert_query, (user.created_at,user.username, user.password, user.target_accurate))
    
    conn.commit()
    conn.close()
    
    # influx에 user 생성
    inf_query = """CREATE USER %s WITH PASSWORD '%s';
    GRANT WRITE ON user_value TO %s;""" % (user.username, user.password,user.username)
    inf_db.query(inf_query)
    
    return {"message": "UserInfo created successfully"}

# 특정 사용자 조회 함수
@router.get("/{user_id}")
async def get_user(user_id: int):
    conn = tool.login_admin_mysql()
    cursor = conn.cursor()
    select_query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(select_query, user_id)
    result = cursor.fetchone()
    conn.close()
    if result:
        user = {
            "id": result[0],
            "created_at":result[1],
            "username": result[2],
            "password": result[3],
            "result": result[4],
            "target_accurate": result[5],
            "flag": result[6],
            "activation": result[7]
        }
        return user
    else:
        return {"message": "UserInfo not found"}

# 특정 사용자 업데이트 함수
@router.put("/{user_id}")
async def update_user(user_id: int, user: UserInfo):
    conn = tool.login_admin_mysql()
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

# 특정 사용자 삭제 함수
@router.delete("/{user_id}")
async def delete_user(user_id: int):
    conn = tool.login_admin_mysql()
    cursor = conn.cursor()
    delete_query = "DELETE FROM users WHERE id = %s"
    cursor.execute(delete_query, user_id)
    conn.commit()
    conn.close()
    return {"message": "UserInfo deleted successfully"}

