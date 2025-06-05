from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.api.schemas.auth import LoginRequest, TokenResponse
from app.services.auth import login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    token = login_user(db, login_data.email, login_data.password)
    return {"access_token": token, "token_type": "bearer"}
