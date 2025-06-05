from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemas.user import UserCreate, UserResponse
from app.services.user import create_user
from app.db.dependency import get_db
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # You can add checks for duplicates here if needed
    return create_user(db, user)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user