from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session 
from . import models, schema,utils
from .databse import engine,get_db
from. routers import post , user,auth


models.Base.metadata.create_all(bind = engine)

app = FastAPI()



while True:

    try:
        conn = psycopg2.connect(host='localhost',database ='fastapi',user='postgres',password='rosan@1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was Sucessfull")
        break
    except Exception as error : 
        print("Connection to Databse Failed")
        print("Error",error)
        time.sleep(2)


my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"Favroit food", "content":"I like pizza","id":2}]



def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
         if p['id'] == id:
            return i 


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return{"message":"Hello welcome to mt API....."}

 