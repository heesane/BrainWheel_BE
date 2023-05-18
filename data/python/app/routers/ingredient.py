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
router = APIRouter(prefix="/ingredient", tags=["ingredient"])

@router.get("/")
async def ingredient_mainpage():
    return "Ingredient Router"

# 식재료 전체 보기 API
@router.get("/show")
async def get_ingredients():
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 실행
            sql = "SELECT * FROM ingredients"
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
    
# 특정 식재료 조회 API
@router.get("/{ingredient_name}")
async def get_ingredient(ingredient_name: str):
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # SQL 쿼리 실행
            sql = "SELECT * FROM ingredients WHERE name = %s"
            cursor.execute(sql, (ingredient_name))

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
    
# 식재료 등록 API
@router.post("/register")
async def register_ingredient(ingredient: models.Ingredient):
    
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # 음식 등록 SQL 쿼리 실행
            sql = """
            INSERT INTO ingredients (name, price, amount) VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (ingredient.name, ingredient.price, ingredient.amount))
            # DB에 반영
            conn.commit()
            # 결과 반환
            return {"message": "Success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

# 식재료 수정 API
@router.put("/update")
async def update_ingredient(ingredient: models.Ingredient):
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # 음식 수정 SQL 쿼리 실행
            sql = """
            UPDATE ingredients SET name = %s, price = %s, amount = %s WHERE name = %s
            """
            cursor.execute(sql, (ingredient.name, ingredient.price, ingredient.amount, ingredient.name))
            # DB에 반영
            conn.commit()
            # 결과 반환
            return {"message": "Success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

# 식재료 삭제 API
@router.delete("/delete")
async def delete_ingredient(ingredient_name: str):
    conn = tool.login_admin_mysql()
    try:
        with conn.cursor() as cursor:
            # 음식 삭제 SQL 쿼리 실행
            sql = """
            DELETE FROM ingredients WHERE name = %s
            """
            cursor.execute(sql, (ingredient_name))
            # DB에 반영
            conn.commit()
            # 결과 반환
            return {"message": "Success"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()