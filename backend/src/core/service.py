from sqlmodel.ext.asyncio.session import AsyncSession

from core.repository import BaseRepository

class BaseService:
    repository: BaseRepository = None

    def __init__(self, session: AsyncSession = None) -> None:
        self.session = session

    async def get_all(self):
        return await self.repository(self.session).get_all()
    
    async def get_by_id(self, id: str):
        return await self.repository(self.session).get_by_id(id)
    
    async def add(self, **values):
        return await self.repository(self.session).add(**values)
    
    async def delete(self, id: str):
        return await self.repository(self.session).delete(id)

    async def update(self, id: str, **values):
        return await self.repository(self.session).update(id, **values)