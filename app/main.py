from fastapi import FastAPI,Response,status,HTTPException
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
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: post): 
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}") ##{id} it is a path parameter 
def get_post(id:int): #,response:Response use this when you use the response module 
    post = find_post(int(id))
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
    index = find_index_post(id)
    if index == none:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update post
@app.put("/posts/{id}")
def update_post(id:int,post:post):
    index = find_index_post(id)
    if index == none:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    post_dict = post.dict()
    post_dict["id"]= id
    my_posts[index]=post_dict
    return{"data":post_dict}

