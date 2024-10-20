from admin.model import RequestModel
import bcrypt
from fastapi.security import OAuth2PasswordBearer

from admin.schemas import SAdminCreate, SRequestCreate, SUserCreate
from service import BaseService
from admin.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AdminService(BaseService):
    repository = UserRepository

    async def get_by_login(self, login: str):
        return await self.repository(self.session).get_by_login(login)
    
    async def get_all_requests(self):
        return await self.repository(self.session).get_all_requests()

    async def add(self, user: SUserCreate | SAdminCreate):
        user.password = self.hash_password(user.password)
        return await self.repository(self.session).add(**user.model_dump())
    
    async def add_request(self, request: SRequestCreate) -> RequestModel:
        return await self.repository(self.session).add_request(request)

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    @staticmethod
    def verify_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

