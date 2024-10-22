from abc import ABC
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
    DataError,
    ProgrammingError,
    OperationalError,
)


class BaseRepository(ABC):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        pass

    def error_message(self, e: Exception) -> str:
        return e

    async def handle_db_error(self, e: Exception, session: AsyncSession):
        await session.rollback()
        if isinstance(e, IntegrityError):
            # Handling data integrity errors (e.g. duplicate unique values)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=self.error_message(e)
            )
        elif isinstance(e, NoResultFound):
            # Not Found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=self.error_message(e)
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

    async def get_all(self):
        try:
            query = select(self.model)
            result = await self.session.exec(query)
            return result.all()
        except Exception as e:
            await self.handle_db_error(e, self.session)

    async def get_by_id(self, id: str):
        try:
            query = select(self.model).filter_by(id=id)
            result = await self.session.exec(query)
            return result.one()
        except Exception as e:
            await self.handle_db_error(e, self.session)

    async def add(self, **values):
        try:
            new_instance = self.model(**values)
            self.session.add(new_instance)
            await self.session.commit()
        except Exception as e:
            await self.handle_db_error(e, self.session)
        return new_instance

    async def delete(self, id: str):
        try:
            query = select(self.model).filter_by(id=id)
            result = await self.session.exec(query)
            instanse = result.one()
            await self.session.delete(instanse)
            await self.session.commit()
        except Exception as e:
            await self.handle_db_error(e, self.session)
        return instanse

    async def update(self, id: str, **values):
        try:
            query = select(self.model).filter_by(id=id)
            result = await self.session.exec(query)
            instance = result.one()
            for key, value in values.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            self.session.add(instance)
            await self.session.commit()
        except Exception as e:
            return await self.handle_db_error(e, self.session)
        return instance
