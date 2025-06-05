from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemas.user import UserCreate, UserResponse
from app.services.user import create_user
from app.db.dependency import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # You can add checks for duplicates here if needed
    return create_user(db, user)
