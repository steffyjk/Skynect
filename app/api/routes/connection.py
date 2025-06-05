from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.core.deps import get_current_user
from app.api.schemas.connection import ConnectionRequestCreate, ConnectionResponse
from app.services.connection import send_connection_request
from app.models.user import User
from fastapi import Query
from app.services.connection import respond_to_connection_request, list_pending_requests, remove_connection

router = APIRouter(prefix="/connections", tags=["Connections"])

@router.post("/", response_model=ConnectionResponse)
def request_connection(
    request: ConnectionRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return send_connection_request(db, current_user.id, request.to_user_id)



@router.post("/{request_id}/respond", response_model=ConnectionResponse)
def respond_connection(
    request_id: int,
    accept: bool = Query(..., description="Accept=true or Reject=false"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return respond_to_connection_request(db, current_user.id, request_id, accept)

@router.get("/pending", response_model=list[ConnectionResponse])
def get_pending_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_pending_requests(db, current_user.id)

@router.delete("/{connection_id}")
def delete_connection(
    connection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_connection(db, current_user.id, connection_id)