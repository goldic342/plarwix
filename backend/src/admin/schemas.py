from typing import Optional
import uuid
from pydantic import BaseModel, field_validator

from admin.model import RequestStatus, UserBase
from utils.validators import check_is_alpha
from admin.validators import validate_login, validate_password


class SUserCreate(UserBase):
    password: str | bytes
    _is_alpha = field_validator("first_name", "last_name", "second_name")(
        check_is_alpha
    )
    _validate_login = field_validator("login")(validate_login)
    _validate_password = field_validator("password")(validate_password)


class SUser(UserBase):
    id: uuid.UUID


class SAdminCreate(UserBase):
    password: str | bytes


class SRequestCreate(BaseModel):
    message: str


class SRequestUpdate(BaseModel):
    status: RequestStatus
    handled_by_user_id: uuid.UUID


class SUserUpdate(UserBase):
    password: Optional[str] = None
