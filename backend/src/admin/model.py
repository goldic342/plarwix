from enum import Enum
from typing import Optional
import uuid

from sqlmodel import Field, SQLModel
from database import Base, uuid_id


class UserBase(SQLModel):
    id: Optional[uuid.UUID] = uuid_id
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    second_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    login: str = Field(index=True, unique=True, min_length=1, max_length=50)
    is_superuser: bool = Field(default=False)


class UserModel(Base, UserBase, table=True):
    __tablename__ = "users"
    password: bytes = Field(min_length=1)

class RequestStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    PENDING = "PENDING"

class RequestModel(SQLModel, table=True):
    __tablename__ = "requests"

    id: Optional[uuid.UUID] = uuid_id
    message: str = Field(min_items=1)
    status: RequestStatus
