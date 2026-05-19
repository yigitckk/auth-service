from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import auth as auth_service
from app.schemas.refreshtoken import RefreshTokenRequest
from app.schemas.blacklist import LogoutRequest
from app.core.security import create_access_token, rate_limit, verify_token 

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = auth_service.create_user(db,user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db), _: None = Depends(rate_limit)):
    try:
        token = auth_service.login_user(db, email,password)
        return {"access_token": token, "token_type": "bearer"}   
    except ValueError as e: 
        raise HTTPException(status_code=401, detail=str(e))
  

@router.post("/refresh")
def refresh(token: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        payload = auth_service.get_refresh_token(db, token.refresh_token)
        new_token = create_access_token({"sub": payload["sub"]})
        return {"access_token": new_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/revoke")
def revoke(token: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        auth_service.revoke_refresh_token(db, token.refresh_token)
        return {"message": "Token revoked"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/revoke-all")
def revoke_all(token: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        payload = verify_token(token.refresh_token)
        user_id = int(payload["sub"])
        auth_service.revoke_all(db,user_id)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=strstr(e))


@router.post("/logout")
def logout(token: LogoutRequest, db:Session = Depends(get_db)):
    try:
        # İşi tamamen service katmanına (service_auth.py) bırakıyoruz
        auth_service.logout_user(token=token.access_token, db=db)
        
        # İşlem başarılıysa sadece mesaj döndür
        return {"message": "Başarıyla çıkış yapıldı."}
        
    except ValueError as e:
        # Token hatalı veya süresi dolmuşsa service_auth'dan fırlatılan hatayı yakala
         raise HTTPException(
            status_code=401, 
            detail=str(e)
        )
