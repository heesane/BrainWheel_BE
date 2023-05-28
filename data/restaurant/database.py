from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# database.py is used to create a database session for the application.
# The session is a core SQLAlchemy concept and is a way to keep track of
# url = <id>:<password>@<host ip>:<port>/<database name>?charset=utf8mb4
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://hhs:5499458k@3.216.219.9:3306/restaurant?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()