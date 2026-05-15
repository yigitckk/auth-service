from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = auth_service.create_user(db,user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    try:
        token = auth_service.login_user(db, email,password)
        return {"access_token": token, "token_type": "bearer"}   
    except ValueError as e: 
        raise HTTPException(status_code=401, detail=str(e))
   
