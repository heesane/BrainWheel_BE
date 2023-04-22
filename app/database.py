from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
id = 'hhs'
pwd = '5499458kK@'
server_ip = "54.161.89.71"
SQLALCHEMY_DATABASE_URL = f"pymysql+aqlalchemy://{id}:{pwd}@{server_ip}/test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()