from pydantic import BaseModel, field_validator
from sqlmodel import Field

from admin.model import RequestStatus, UserBase
from utils import check_is_alpha
from admin.validators import validate_login, validate_password


class SUserCreate(UserBase):
    password: str
    _is_alpha = field_validator('first_name', 'last_name', 'second_name')(check_is_alpha)
    _validate_login = field_validator('login')(validate_login)
    _validate_password = field_validator('password')(validate_password)

class SAdminCreate(UserBase):
    password: str

class SRequestCreate(BaseModel):
    message: str

class SRequestUpdate(BaseModel):
    id: str
    status: RequestStatus

    