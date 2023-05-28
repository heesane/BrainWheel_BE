from fastapi import FastAPI,Request
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import os

from datetime import datetime


import routers

# CORS URL 설정
origins = [
    "http://*:80",
    "http://*:443",
]

# FastAPI 객체 생성
app = FastAPI(
    title = "BrainWheel Backend API Server",
    description = "BrainWheel Backend API Server",
    version = "1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 요청 정보 추출
    method = request.method
    url = request.url
    client_ip = request.client.host
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 로그 메시지 생성
    log_message = f"[{timestamp}] IP: {client_ip} - Method: {method} - URL: {url}\n"

    # 로그 파일에 기록
    with open("server_log.txt", "a") as log_file:
        log_file.write(log_message)

    response = await call_next(request)
    return response

# user router
app.include_router(routers.user_router)
app.include_router(routers.task_router)

app.mount("/assets", StaticFiles(directory="front/dist/assets"))



# mainpage
@app.get("/")
async def mainpage():
    return FileResponse("front/dist/index.html")

