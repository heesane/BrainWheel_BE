from fastapi import FastAPI,Request
from datetime import datetime
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.answer import answer_router
from domain.question import question_router
from domain.user import user_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://*:80",
    "http://*:443",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

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
    with open("server.txt", "a") as log_file:
        log_file.write(log_message)

    response = await call_next(request)
    return response

@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")

@app.get("/log")
def admin():
    return FileResponse("server.txt")