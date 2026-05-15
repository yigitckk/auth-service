from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token

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
    return token
