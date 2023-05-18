# pip install ~~
from typing import Optional
from fastapi import FastAPI,Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from influxdb import client as influxdb
import pymysql
import os
from datetime import datetime

# My Module
import tool
from tool import inf_db, login_admin_mysql,make_csv,training
from models import UserInfo, Food
from routers import user_router, restaurant_router

inf_db = inf_db

app = FastAPI()

# user router
app.include_router(user_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 요청 정보 추출
    method = request.method
    url = request.url
    client_ip = request.client.host
    if url == "http://127.0.0.1:5000/restaurants/register":
        conn = login_admin_mysql()
        cur = conn.cursor()
        sql = """INSERT INTO client.info (ip) VALUES(%s);"""
        conn.execute(sql, client_ip)
        conn.commit()
        conn.close()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 로그 메시지 생성
    log_message = f"[{timestamp}] IP: {client_ip} - Method: {method} - URL: {url}\n"

    # 로그 파일에 기록
    with open("server_log.txt", "a") as log_file:
        log_file.write(log_message)

    response = await call_next(request)
    return response

# mainpage
@app.get("/")
async def mainpage():
    return "BrainWheel Backend API Server"

# Flag 수신 처리 함수
@app.get("/flag/{user_name}")
async def ReceiveFlag(user_name: str, flag: str):
    # Flag: inf_success -> csv_success -> h5_success
    if flag == "inf_success":
        while make_csv(user_name) != True:
            continue
        csv_flag =True
        return {"flag": "Make CSV Success"}
    
    elif flag == "csv_success":
        first_csv = user_name + "_first.csv"
        second_csv = user_name + "_second.csv"
        weight_file = user_name + ".h5"
        while training(first_csv,second_csv,weight_file) != True:
            continue
        h5_flag = True
        return {"flag": "Make H5 Success"}

# h5 파일 다운로드 함수
@app.get("/download/{user_id}")
async def download_h5(user_id: str):
    file_path = "h5_file/" + str(user_id) + ".h5"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/hdf5', filename=str(user_id) + ".h5")
    else:
        return {"message": "File not found."}

# 성공 여부 저장
@app.get("/end/{user_name}/success")
async def end_success(user_name: str):
    conn = login_admin_mysql()
    cur = conn.cursor()
    sql = """UPDATE `userinfo`.`users` SET `flag` = '1', `activation` = `True` WHERE (`username` = %s);"""
    conn.execute(sql, user_name)
    conn.commit()
    conn.close()
    return {"message": "You Can Use BrainWheel"}

# 정확도 측정 결과
@app.post("/end")
async def end_result(user_name: str, result: int):
    conn =login_admin_mysql()
    cur = conn.cursor()
    sql = """UPDATE `userinfo`.`users` SET `result` = %d WHERE (`username` = %s);"""
    conn.execute(sql, result, user_name)
    conn.commit()
    conn.close()
    return {"message": "Almost done"}

