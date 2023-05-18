from typing import Optional
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import FileResponse
from influxdb import client as influxdb
import pymysql
from pydantic import BaseModel
import os
import datetime

import models
import tool

router = APIRouter(prefix="/table", tags=["table"])

def send():
    pass
## Describe Table
# id: int
# people: int
# food : json
# total_price: int
# is_empty: bool

@router.get("/")
async def table_mainpage():
    return "Table Router"

# 전체 테이블 조회 API
@router.get("/show")
async def get_tables():
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 실행
            sql = "SELECT * FROM tables"
            cursor.execute(sql)

            # 결과 가져오기
            result = cursor.fetchall()
            if result:
                return result
            else:
                {"message":"Not Found Food Data"}
            return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
        
    
# 특정 테이블 조회 API
@router.get("/{table_id}")
async def get_table(table_id: int):
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 실행
            sql = "SELECT * FROM tables WHERE id = %s"
            cursor.execute(sql, (table_id))

            # 결과 가져오기
            result = cursor.fetchall()
            if result:
                return result
            else:
                {"message":"Not Found Food Data"}
            return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
        

# 식당 내 테이블 초기화
@router.get("/init")
async def init_tables(number: int):
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 실행
            for i in range(1,number+1):
                sql = "INSERT INTO tables (id, people, food, total_price, is_empty) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (i, 0, "[]", 0, True))
            conn.commit()
            return {"message":"Success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
        
@router.get("/order")
async def order(table:models.Table):
    table_num = table.table_number
    people = table.people
    food = table.food
    total_price = table.total_price
    is_empty = table.is_empty
    
    is_empty = False
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 실행
            sql = "UPDATE tables SET people = %s, food = %s, total_price = %s, is_empty = %s WHERE id = %s"
            cursor.execute(sql, (people, food, total_price, is_empty, table_num))
            conn.commit()
            return {"message":"Success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@router.get("/exit")
async def exit(table_id: int):
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 실행
            sql = "UPDATE tables SET people = %s, food = %s, total_price = %s, is_empty = %s WHERE id = %s"
            cursor.execute(sql, (0, "[]", 0, True, table_id))
            conn.commit()
            return {"message":"Success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
        
@router.get("/call")
async def call(call_content:models.Call):
    table_id = call_content.table_id
    content = call_content.content
    amount = call_content.amount
    
    text = f"테이블 {table_id}번에서 {content}을/를 {amount}개를 요청합니다."
    send(text)
    