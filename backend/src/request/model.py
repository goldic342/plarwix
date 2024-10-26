from enum import Enum
from typing import Optional
import uuid

from sqlmodel import Field, Relationship, SQLModel

from database import uuid_id


class RequestStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    PENDING = "PENDING"


class RequestModel(SQLModel, table=True):
    __tablename__ = "requests"

    id: Optional[uuid.UUID] = uuid_id
    message: str = Field(min_length=1)
    status: Optional[RequestStatus] = Field(default=RequestStatus.PENDING)
    handled_by_user_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.id"
    )
    handled_by_user: Optional["UserModel"] = Relationship(back_populates="requests")

from admin.model import UserModel