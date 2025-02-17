from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

#This is the url for connecting to the database using orm
#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip address/hostname>/< database_name>"
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:rosan@1234@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:@localhost/fastapi'



engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:  
        db.close()

# while True:

#     try:
#         conn = psycopg2.connect(host='localhost',database ='fastapi',user='postgres',password='rosan@1234', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database Connection was Sucessfull")
#         break
#     except Exception as error : 
#         print("Connection to Databse Failed")
#         print("Error",error)
#         time.sleep(2)