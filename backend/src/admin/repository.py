from admin.schemas import SRequestCreate
from sqlmodel import select
from admin.model import RequestModel, RequestStatus, UserModel
from repository import BaseRepository
from sqlalchemy.exc import IntegrityError, NoResultFound


class UserRepository(BaseRepository):
    model = UserModel

    def error_message(self, e: Exception):
        if isinstance(e, IntegrityError):
            return "The user with this login already exists"
        elif isinstance(e, NoResultFound):
            return "The user did not found"
        else:
            return e

    async def get_by_login(self, login):
        try:
            query = select(self.model).filter_by(login=login)
            result = await self.session.exec(query)
            return result.one()
        except Exception as e:
            self.handle_db_error(e, self.session)

    async def get_all_requests(self):
        try:
            query = select(RequestModel).filter_by(status=RequestStatus.PENDING)
            result = await self.session.exec(query)
            return result.all()
        except Exception as e:
            self.handle_db_error(e, self.session)

    async def add_request(self, request: SRequestCreate):
        try:
            request = RequestModel(message=request.message, status=RequestStatus.PENDING)
            self.session.add(request)
            await self.session.commit()
        except Exception as e:
            await self.handle_db_error(e, self.session)
        return request