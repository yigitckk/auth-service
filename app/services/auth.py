from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.models.refreshtoken import RefreshToken 
from app.schemas.refreshtoken import RefreshTokenRequest 
from app.core.security import hash_password, verify_password, create_access_token, generate_refresh_token, verify_token

def create_user(db: Session, user:UserCreate) -> User:
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise ValueError("Email registered")
    hashed_pass = hash_password(user.password)
    db_user = User(
        email = user.email,
        full_name = user.full_name,
        hashed_password = hashed_pass
    ) 
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db:Session, email:str, password:str) -> User | None:
    authed = db.query(User).filter(User.email == email).first()
    if not authed: 
        return None
    if not verify_password(password,authed.hashed_password):
        return None
    return authed 


def login_user(db:Session, email: str, password:str) -> dict:
    user = authenticate_user(db,email,password)
    if not user:
        raise ValueError("Invalid credentials")

    token = create_access_token({"sub": user.email})
    refresh_token = save_refresh_token(db, user.id)
    return {"access_token": token, "refresh_token": refresh_token}


def save_refresh_token(db: Session, user_id: int) -> RefreshToken:
    gtoken = generate_refresh_token({"sub": str(user_id)})
    db_token = RefreshToken(token=gtoken, user_id=user_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def revoke_refresh_token(db: Session, token: dict):
    token = db.query(RefreshToken).filter(RefreshToken.token == token).first() # silmem lazım direkt tek atırda ama db.remove mu 
    if token is None:
        raise ValueError("Invalid token")
    db.delete(token)
    db.commit()



def get_refresh_token(db, token):
    refresh_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not refresh_token:
        raise ValueError("INvalid credentials")
    verified = verify_token(refresh_token.token)
    return verified
    
