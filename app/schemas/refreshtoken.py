from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class RefreshTokenRequest(BaseModel):
    refresh_token: str 
