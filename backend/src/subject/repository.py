from pydantic import BaseModel
from utils.errors import NoResultFound
from pymongo.errors import DuplicateKeyError
from core.mongodb_repository import BaseMongoRepository
from database import mongo_db


class SubjectRepository(BaseMongoRepository):
    collection = mongo_db.subject

    @classmethod
    def error_message(cls, e: Exception) -> str | Exception:
        if isinstance(e, DuplicateKeyError):
            return "The subject already exist"
        elif isinstance(e, NoResultFound):
            return "The subject not found"
        else:
            return e
        
    @classmethod
    async def add(cls, obj: BaseModel, unique: dict | None = None):
        try:
            result = await cls.collection.insert_one(obj.model_dump(by_alias=True))
            return result
        except Exception as e:
            cls.handle_db_error(e)
    
