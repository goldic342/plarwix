from enum import Enum
from typing import List, Optional
import uuid

from sqlmodel import Field, Relationship, SQLModel
from database import Base, uuid_id


class UserBase(SQLModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    second_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    login: str = Field(index=True, unique=True, min_length=1, max_length=50)
    is_superuser: bool = Field(default=False)


class UserModel(Base, UserBase, table=True):
    __tablename__ = "users"

    id: Optional[uuid.UUID] = uuid_id
    password: bytes = Field(min_length=1)

    requests: list["RequestModel"] = Relationship(back_populates="handled_by_user")


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
    handled_by_user: Optional[UserModel] = Relationship(back_populates="requests")
