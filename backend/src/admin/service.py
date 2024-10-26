import uuid
from fastapi.security import OAuth2PasswordBearer

from admin.schemas import (
    SAdminCreate,
    SUser,
    SUserCreate,
)
from admin.utils import hash_password
from core.service import BaseService
from admin.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AdminService(BaseService):
    repository = UserRepository

    async def add(self, user: SUserCreate | SAdminCreate) -> SUser:
        user.password = hash_password(user.password)
        result = await self.repository(self.session).add(**user.model_dump())
        return result

    async def update(self, id: uuid.UUID, **values):
        password = values.get("password")
        if password is not None:
            values["password"] = hash_password(password)
        else:
            values.pop("password")
        return await self.repository(self.session).update(str(id), **values)

    async def get_by_login(self, login: str) -> SUser:
        return await self.repository(self.session).get_by_login(login)

