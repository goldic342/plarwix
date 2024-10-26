from utils.errors import NoResultFound
from pymongo.errors import DuplicateKeyError
from core.mongodb_repository import BaseMongoRepository
from database import mongo_db


class ClasRepository(BaseMongoRepository):
    collection = mongo_db["class"]

    @classmethod
    def error_message(cls, e: Exception) -> str | Exception:
        if isinstance(e, DuplicateKeyError):
            return "The class already exist"
        elif isinstance(e, NoResultFound):
            return "The class not found"
        else:
            return e
    
