from sqlalchemy import Column, Integer, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.db.session import Base

class ConnectionStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class ConnectionRequest(Base):
    __tablename__ = "connection_requests"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(SqlEnum(ConnectionStatus), default=ConnectionStatus.pending)

    from_user = relationship("User", foreign_keys=[from_user_id])
    to_user = relationship("User", foreign_keys=[to_user_id])
