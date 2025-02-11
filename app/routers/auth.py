from fastapi import  APIRouter,Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import databse , schema ,models,utils ,oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login( user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(databse.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= f"Invalid crediantals")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= f"Invalid cridentatials")
    

    acess_token = oauth2.create_acess_token(data={"user_id":user.id})

    return {"acess_token": acess_token, "token_type":"bearer"}