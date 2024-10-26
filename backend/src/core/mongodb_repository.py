from abc import ABC
import uuid

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError
from sqlalchemy.exc import (
    DataError,
    ProgrammingError,
    OperationalError,
)

from utils.errors import NoResultFound


class BaseMongoRepository(ABC):
    collection: AsyncIOMotorCollection = None

    @classmethod
    def error_message(cls, e: Exception) -> str | Exception:
        return

    @classmethod
    def handle_db_error(cls, e: Exception):
        if isinstance(e, DuplicateKeyError):
            # Handling data integrity errors (e.g. duplicate unique values)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=cls.error_message(e)
            )
        elif isinstance(e, NoResultFound):
            # Not Found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=cls.error_message(e)
            )
        elif isinstance(e, DataError):
            # Bad Request
            print(f"Ar error occured: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect data"
            )
        elif isinstance(e, ProgrammingError):
            # Internal Server Error
            print(f"Ar error occured: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )
        elif isinstance(e, OperationalError):
            # Service Unavailable
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection error",
            )
        else:
            # Unknown error
            raise e

    @classmethod
    async def get_all(cls):
        try:
            cursor = cls.collection.find()
            documents = await cursor.to_list(length=None)
            return documents
        except Exception as e:
            cls.handle_db_error(e)
        return documents

    @classmethod
    async def get_by_id(cls, id: uuid.UUID):
        try:
            document = await cls.collection.find_one({"_id": str(id)})
            if document is None:
                raise NoResultFound
            return document
        except Exception as e:
            cls.handle_db_error(e)

    @classmethod
    async def add(cls, obj: BaseModel, unique: dict | None = None):
        try:
            if unique:
                document = await cls.collection.find_one(unique)
                if document:
                    raise DuplicateKeyError("Duplicate error")
            result = await cls.collection.insert_one(obj.model_dump(by_alias=True))
            return result
        except Exception as e:
            cls.handle_db_error(e)

    @classmethod
    async def update(cls, obj: BaseModel, id: uuid.UUID):
        try:
            document = await cls.collection.find_one_and_update({"_id": str(id)}, { "$set": obj.model_dump(by_alias=True)})
            if document is None:
                raise NoResultFound
        except Exception as e:
            cls.handle_db_error(e)

    @classmethod
    async def delete(cls, id: uuid.UUID):
        try:
            document = await cls.collection.find_one_and_delete({"_id": str(id)})
            if document is None:
                raise NoResultFound
        except Exception as e:
            cls.handle_db_error(e)
