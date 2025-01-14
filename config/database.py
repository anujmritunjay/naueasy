import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")  
MYSQL_PORT = os.getenv("MYSQL_PORT", 3306) 
MYSQL_USER = os.getenv("MYSQL_USER", "root") 
MYSQL_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD", "admin")) 
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "events")
SQLALCHEMY_DATABASE_URL = F"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
print("lakf00", SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=5, max_overflow=10, pool_timeout=30, pool_recycle=1800)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()