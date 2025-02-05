from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()


class post(BaseModel):
    title: str
    content:str
    published:bool=True
    rating : Optional[int]= None

my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"Favroit food", "content":"I like pizza","id":2}]

@app.get("/")
async def root():
    return{"message":"Hello welcome to mt API....."}

@app.get("/posts")    
def get_posts():
    return{"data":my_posts}


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
@app.post("/posts")
def create_posts(post: post): 
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}") ##{id} it is a path parameter 
def get_post(id):
    print(id)
    return{"post details":f"Here is post{id}"}