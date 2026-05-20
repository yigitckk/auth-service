from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class SessionResponse(BaseModel):
    id: int
    ip_address: str
    user_agent:  Optional[str] = None
    created_at: datetime
    is_active: bool




