from sqlalchemy import Column, Integer, String, Boolean, DateTime 
from sqlalchemy.sql import func
from app.db.database import Base 
from datetime import datetime, timedelta

class Session(Base):

    __tablename__ = "sessions" #database tablo name 
   
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    ip_address = Column(String, index=True, nullable=False)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), default=lambda: datetime.utcnow() + timedelta(days=7))
    is_active = Column(Boolean,default=True)

    def __repr__(self):
        return f"<Session(user_id={self.user_id}, ip={self.ip_address})>"


