from abc import ABC
import uuid
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from core.repository import BaseRepository

class BaseService(ABC):
    repository: BaseRepository = None

    def __init__(self, session: AsyncSession = None) -> None:
        self.session = session

    async def get_all(self):
        return await self.repository(self.session).get_all()
    
    async def get_by_id(self, id: uuid.UUID):
        return await self.repository(self.session).get_by_id(str(id))
    
    async def add(self, obj: BaseModel):
        return await self.repository(self.session).add(**obj.model_dump())
    
    async def delete(self, id: uuid.UUID):
        return await self.repository(self.session).delete(str(id))

    async def update(self, id: uuid.UUID, obj: BaseModel):
        return await self.repository(self.session).update(str(id), **obj.model_dump())