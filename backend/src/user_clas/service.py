import uuid
from user_clas.schemas import SUserClas
from user_clas.repository import UserClasRepository


class UserClasService:
    repository = UserClasRepository

    @classmethod
    async def get_clases_by_user_id(cls, user_id: uuid.UUID) -> list[SUserClas]:
        return await cls.repository.get_clases_by_user_id(str(user_id))
    
    @classmethod
    async def add_user_clases(cls, user_id: uuid.UUID, clases_ids: set[uuid.UUID]):
        await cls.repository.add_user_clases(str(user_id), map(str, clases_ids))

    @classmethod
    async def update_user_clases(cls, user_id: uuid.UUID, clases_ids: set[uuid.UUID]):
        user_id = str(user_id)
        await cls.repository.delete_by_user_id(user_id)
        await cls.repository.add_user_clases(user_id, map(str, clases_ids))

    @classmethod
    async def delete_by_clas_id(cls, clas_id: uuid.UUID):
        await cls.repository.delete_by_clas_id(str(clas_id))

    @classmethod
    async def delete_by_user_id(cls, user_id: uuid.UUID):
        await cls.repository.delete_by_user_id(str(user_id))