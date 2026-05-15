from sqlalchemy import Column, Integer, String, Boolean, DateTime 
from sqlalchemy.sql import func
from app.db.database import Base 

class User(Base):

    __tablename__ = "users" #database tablo name 

    id = Column(Integer,primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String,nullable=False) #düz metin tutulamaz!

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(email={self.email})>"

