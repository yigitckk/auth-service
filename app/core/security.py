from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from collections import defaultdict
from fastapi import HTTPException, Request

def hash_password(password: str) -> str:
    return pwd_context.hash(password) # hash üretimi.
def verify_password(plain_password:str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    kopya = data.copy()
    kopya["exp"] = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    imza = jwt.encode(kopya,settings.SECRET_KEY, algorithm=settings.ALGORITHM) #imza 
    return imza

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    except JWTError as e:
        raise JWTError("Could not validate token")

def generate_refresh_token(data: dict) -> str:
    kopya = data.copy()
    kopya["exp"] = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    imza = jwt.encode(kopya,settings.SECRET_KEY, algorithm=settings.ALGORITHM) #imza 
    return imza

rate_limit_store = {} #[count, window_start]

def rate_limit(request: Request):
    ip = request.client.host
    if ip in rate_limit_store:
        count, window_start = rate_limit_store[ip]
        if datetime.utcnow() - window_start > timedelta(minutes=5): 
            window_start = datetime.utcnow()
            count = 1
        else: 
            count += 1
        rate_limit_store[ip] = [count,datetime.utcnow()]

        if count > 5:
            raise HTTPException(status_code=429)
    else:
        rate_limit_store[ip] = [1, datetime.utcnow()]





