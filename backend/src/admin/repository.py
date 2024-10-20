from admin.schemas import SRequestCreate, SRequestUpdate
from sqlmodel import select
from admin.model import RequestModel, RequestStatus, UserBase, UserModel
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

    async def get_by_login(self, login) -> UserBase:
        try:
            query = select(self.model).filter_by(login=login)
            result = await self.session.exec(query)
            return result.one()
        except Exception as e:
            self.handle_db_error(e, self.session)

    async def get_all_requests(self) -> list[RequestModel]:
        try:
            query = select(RequestModel).filter_by(status=RequestStatus.PENDING)
            result = await self.session.exec(query)
            return result.all()
        except Exception as e:
            self.handle_db_error(e, self.session)

    async def add_request(self, request: SRequestCreate) -> RequestModel:
        try:
            request = RequestModel(message=request.message, status=RequestStatus.PENDING)
            self.session.add(request)
            await self.session.commit()
        except Exception as e:
            await self.handle_db_error(e, self.session)
        return request
    
    async def update_request(self, request: SRequestUpdate) -> RequestModel:
        try:
            query = select(RequestModel).filter_by(id=request.id)
            result = await self.session.exec(query)
            instance = result.one()
            instance.status = request.status
            self.session.add(instance)
            await self.session.commit()
        except Exception as e:
            await self.handle_db_error(e, self.session)
        return instance