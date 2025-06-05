from pydantic import BaseModel
from enum import Enum

class ConnectionStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class ConnectionRequestCreate(BaseModel):
    to_user_id: int

class ConnectionResponse(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    status: ConnectionStatus

    class Config:
        orm_mode = True
