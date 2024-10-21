import uuid
from admin.model import RequestModel, RequestStatus, UserBase, UserModel
from fastapi.security import OAuth2PasswordBearer

from admin.schemas import SAdminCreate, SRequestCreate, SRequestUpdate, SUserCreate
from admin.utils import hash_password
from core.service import BaseService
from admin.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AdminService(BaseService):
    repository = UserRepository

    async def get_by_login(self, login: str) -> UserBase:
        return await self.repository(self.session).get_by_login(login)
    
    async def get_all_requests(self, filter_by_status: RequestStatus | None = None, filter_by_user_id: uuid.UUID | None = None) -> list[RequestModel]:
        return await self.repository(self.session).get_all_requests(filter_by_status, filter_by_user_id)

    async def add(self, user: SUserCreate | SAdminCreate) -> UserModel:
        user.password = hash_password(user.password)
        result = await self.repository(self.session).add(**user.model_dump())
        return result
    
    async def update(self, **values):
        password = values.get('password')
        if password is not None:
            values['password'] = hash_password(password)
        else:
            values.pop('password')
        return await self.repository(self.session).update(**values)
    
    async def add_request(self, request: SRequestCreate) -> RequestModel:
        return await self.repository(self.session).add_request(request)
    
    async def update_request(self, request: SRequestUpdate) -> RequestModel:
        result = await self.repository(self.session).update_request(request)
        return result

    

