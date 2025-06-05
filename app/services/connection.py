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

def respond_to_connection_request(db: Session, current_user_id: int, request_id: int, accept: bool):
    conn_request = db.query(ConnectionRequest).filter(
        ConnectionRequest.id == request_id,
        ConnectionRequest.to_user_id == current_user_id,
        ConnectionRequest.status == ConnectionStatus.pending
    ).first()

    if not conn_request:
        raise HTTPException(status_code=404, detail="Connection request not found")

    conn_request.status = ConnectionStatus.accepted if accept else ConnectionStatus.rejected
    db.commit()
    db.refresh(conn_request)
    return conn_request

def list_pending_requests(db: Session, user_id: int):
    return db.query(ConnectionRequest).filter(
        ConnectionRequest.to_user_id == user_id,
        ConnectionRequest.status == ConnectionStatus.pending
    ).all()

def remove_connection(db: Session, current_user_id: int, connection_id: int):
    # Connection removal means deleting accepted connection where current user is from_user or to_user
    conn = db.query(ConnectionRequest).filter(
        ConnectionRequest.id == connection_id,
        ConnectionRequest.status == ConnectionStatus.accepted,
        ((ConnectionRequest.from_user_id == current_user_id) | (ConnectionRequest.to_user_id == current_user_id))
    ).first()

    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found or not authorized")

    db.delete(conn)
    db.commit()
    return {"detail": "Connection removed"}