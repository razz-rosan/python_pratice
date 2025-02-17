from jose import  JWTError,jwt
from datetime import datetime ,timedelta
from . import  schema , databse , models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

#Seceret_key
#Algrothim 
#Expriation time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow()+timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=(ALGORITHM))

    return encoded_jwt


def Verify_access_token(token:str,crediantials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id = str(payload.get("user_id"))
        if id is None :
            raise crediantials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise crediantials_exception
    
    return token_data

def get_current_user(token:str = Depends(oauth2_schema),db:Session = Depends(databse.get_db)):
    crediantials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate crediantials",headers={"WWW-Authenticate":"Bearer"})


    token = Verify_access_token(token , crediantials_exception)
    user = db.query(models.User).filter(models.User.id== token.id).first()
    
    return user