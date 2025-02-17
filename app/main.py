from fastapi import FastAPI
from . import models
from .databse import engine
from. routers import post , user,auth
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    databse_password: str 
    database_username: str = "postgrese"
    secert_key: str = "jgt5667tyuf56tc"

settings = Settings()
print(settings.databse_password)

models.Base.metadata.create_all(bind = engine)

app = FastAPI()



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



@app.get("/")
async def root():
    return{"message":"Hello welcome to mt API....."}

 