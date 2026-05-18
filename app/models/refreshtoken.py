from sqlalchemy import Column, Integer, String, Boolean, DateTime 
from sqlalchemy.sql import func
from app.db.database import Base 
from datetime import datetime, timedelta

class RefreshToken(Base):

    __tablename__ = "refresh_tokens" #database tablo name 
    
    token = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), default=lambda: datetime.utcnow() + timedelta(days=7))
    def __repr__(self):
        return f"<User(email={self.token})>"

