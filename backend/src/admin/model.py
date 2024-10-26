from typing import Optional
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

from request.model import RequestModel

