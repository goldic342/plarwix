from abc import ABC
import uuid

from pydantic import BaseModel

from core.mongodb_repository import BaseMongoRepository


class BaseMongoService(ABC):
    repository: BaseMongoRepository = None
    return_model: BaseModel = None

    @classmethod
    async def get_all(cls) -> list[BaseModel]:
        documents = await cls.repository.get_all()
        return_model_list = [cls.return_model(id=str(document["_id"]), **document) for document in documents]
        return return_model_list

    @classmethod
    async def get_by_id(cls, id: uuid.UUID) -> BaseModel:
        document = await cls.repository.get_by_id(id)
        return cls.return_model(**document)

    @classmethod
    async def add(cls, obj: BaseModel, unique: dict | None = None) -> BaseModel:
        save_obj = cls.return_model(**obj.model_dump())
        await cls.repository.add(save_obj, unique)
    
    @classmethod
    async def update(cls, obj: BaseModel, id: uuid.UUID):
        await cls.repository.update(obj, id)

    @classmethod
    async def delete(cls, id: uuid.UUID):
        await cls.repository.delete(id)
