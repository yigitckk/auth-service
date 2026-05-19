from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import  Base 

class BlacklistedToken(Base):
    __tablename__ = "Blacklisted_tokens"

    user_id = Column(Integer,primary_key=True, index =True)
    token = Column(String,unique = True,index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
