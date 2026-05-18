from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: str 


class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int 

