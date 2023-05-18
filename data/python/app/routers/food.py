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
router = APIRouter(prefix="/food", tags=["food"])

# food router
@router.get("/")
async def food_mainpage():
    return "Food Router"

# 등록된 음식 조회 API
@router.get("")
async def get_all_foods():
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 실행
            sql = "SELECT * FROM foods"
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

# 특정 음식 조회 API
@router.get("/{food_name}")
async def get_food(food_name: str):
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 실행
            sql = "SELECT * FROM foods WHERE name = %s"
            cursor.execute(sql, (food_name))

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
    
# 음식 등록 API
@router.post("/register")
async def register_food(food: models.Food):
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # 음식 등록 SQL 쿼리 실행
            sql = """
            INSERT INTO foods (name, price) VALUES (%s, %s)
            """
            cursor.execute(sql, (food.name, food.price))
            # DB에 반영
            conn.commit()
            # 결과 반환
            return {"message": "Success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

# 음식 수정 API
@router.put("/update")
async def update_food(food: models.Food):
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # 음식 수정 SQL 쿼리 실행
            sql = """
            UPDATE foods SET name = %s, price = %s WHERE name = %s
            """
            cursor.execute(sql, (food.name, food.price, food.name))
            # DB에 반영
            conn.commit()
            # 결과 반환
            return {"message": "Success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

# 음식 삭제 API
@router.delete("/delete")
async def delete_food(food_name: str):
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # 음식 삭제 SQL 쿼리 실행
            sql = """
            DELETE FROM foods WHERE name = %s
            """
            cursor.execute(sql, (food_name))
            # DB에 반영
            conn.commit()
            # 결과 반환
            return {"message": "Success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
