from fastapi import FastAPI
from fastapi.params import Body
app = FastAPI()

@app.get("/")
async def root():
    return{"message":"Hello welcome to mt API....."}

@app.get("/post")    
def get_posts():
    return{"data":"This your post"}

@app.post("/createpost")
def create_posts(payload: dict = Body(...)): ## in this passing parameter we use the variable name payload andassign it as a dictionary so that it wii take arguments as json format
    print(payload) ## this is used to get the data from the post man
    return{"new post":f"title :{payload['title']}  content: {payload['content']}"} 