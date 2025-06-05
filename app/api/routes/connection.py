from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.core.deps import get_current_user
from app.api.schemas.connection import ConnectionRequestCreate, ConnectionResponse
from app.services.connection import send_connection_request
from app.models.user import User

router = APIRouter(prefix="/connections", tags=["Connections"])

@router.post("/", response_model=ConnectionResponse)
def request_connection(
    request: ConnectionRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return send_connection_request(db, current_user.id, request.to_user_id)
