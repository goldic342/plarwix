from admin.schemas import SUser
from sqlmodel import select
from admin.model import UserModel
from core.repository import BaseRepository
from sqlalchemy.exc import IntegrityError, NoResultFound


class UserRepository(BaseRepository):
    model = UserModel

    def error_message(self, e: Exception) -> str | Exception:
        if isinstance(e, IntegrityError):
            return "The user with this login already exists"
        elif isinstance(e, NoResultFound):
            return "The user did not found"
        else:
            return e

    async def get_by_login(self, login) -> SUser:
        try:
            query = select(self.model).filter_by(login=login)
            result = await self.session.exec(query)
            return result.one()
        except Exception as e:
            await self.handle_db_error(e, self.session)
    
    
