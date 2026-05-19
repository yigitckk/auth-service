from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class LogoutRequest(BaseModel):
    refresh_token: str 
    access_token: str
