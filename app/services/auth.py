from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.core.security import verify_password
from app.core.jwt import create_access_token

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return user

def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    access_token = create_access_token({"sub": user.email})
    return access_token
