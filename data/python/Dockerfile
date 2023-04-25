# Dockerfile

# 베이스 이미지 설정
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 라이브러리 설치
COPY requirements.txt /app
RUN pip install -r requirements.txt

# 소스 코드 복사
COPY . /app

# 포트 오픈
EXPOSE 5000

# 실행 명령어 설정
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
