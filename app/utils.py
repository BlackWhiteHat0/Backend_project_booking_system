from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

SECRET_KET = ""

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hashed(password:str) -> str :
    return pwd_context.hash(password)

def verify_password(plain_password:str, hash_password:str) -> str :
    return pwd_context.verify(plain_password, hash_password)


def create_access_token(data:dict, expires_delta:Optional[timedelta]=None, ):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KET, algorithm=ALGORITHM)
    return encoded_jwt