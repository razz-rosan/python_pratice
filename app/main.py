from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session 
from . import models
from .databse import engine,SessionLocal


models.Base.metadata.create_all(bind = engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class post(BaseModel):
    title: str
    content:str
    published:bool=True
    rating : Optional[int]= None
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



@app.get("/")
async def root():
    return{"message":"Hello welcome to mt API....."}


@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    return{"status":"sucess"}

@app.get("/posts")    
def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    return{"data":posts}


"""@app.post("/createpost")
def create_posts(new_post:post): 
    print(new_post)
    print(new_post.dict()) 
    return{"Data":"new Post"}
""" 

"""
app.post("/createpost")
def create_posts(payload: dict = Body(...)): ## in this passing parameter we use the variable name payload andassign it as a dictionary so that it wii take arguments as json format
   print(payload) ## this is used to get the data from the post man
  return{"new post":f"title :{payload['title']}  content: {payload['content']}"} 
"""
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: post): 
    """post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)"""# inserting a new post to the database {post_Dict}

    cursor.execute(""" IINSERT INTO post(title,content,published) VALUES(%s,%s,%s) RETURNING* """,(post.titlr,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": "created post"}

@app.get("/posts/{id}") ##{id} it is a path parameter 
def get_post(id:int): #,response:Response use this when you use the response module 
    cursor.execute("""Select * from posts Where id = %s """,(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
        """
        response.status_code= status.HTTP_404_NOT_FOUND 
        return{'message': f"post with id:{id} was not found"}
        """
    ##print(post)
    return{"post details":post}

# deleting a post

@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #find the index in the array that has the required ID
    # my_posts.pop(index)
    cursor.execute(""" DELETE from posts where id = %s""",(str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")

    my_posts.pop(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update post
@app.put("/posts/{id}")
def update_post(id:int,post:post):
    cursor.execute(""" Update posts set title = %s,content = %s,published = %s RETURNING* """,(str(post.title,post.content,post.published)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    return{"data":updated_post}

