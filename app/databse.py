from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#This is the url for connecting to the database using orm
#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip address/hostname>/< database_name>"
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:rosan@1234@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:@localhost/fastapi'



engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()