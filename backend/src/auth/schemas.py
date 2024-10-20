from pydantic import BaseModel


class SAdminLogin(BaseModel):
    login: str
    password: str