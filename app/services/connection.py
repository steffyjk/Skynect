from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.connection import ConnectionRequest, ConnectionStatus
from app.models.user import User

def send_connection_request(db: Session, from_user_id: int, to_user_id: int):
    if from_user_id == to_user_id:
        raise HTTPException(status_code=400, detail="Cannot connect with yourself")

    existing = db.query(ConnectionRequest).filter(
        ConnectionRequest.from_user_id == from_user_id,
        ConnectionRequest.to_user_id == to_user_id,
        ConnectionRequest.status == ConnectionStatus.pending
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Request already sent")

    req = ConnectionRequest(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        status=ConnectionStatus.pending
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req
