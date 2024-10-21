import uuid
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

    async def get_all_requests(self, filter_by_status: RequestStatus | None, filter_by_user_id: uuid.UUID | None = None) -> list[RequestModel]:
        try:
            query = select(RequestModel)
            if filter_by_status:
               query = query.filter_by(status=filter_by_status)
            if filter_by_user_id:
                query = query.filter_by(handled_by_user_id=filter_by_user_id)
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
            instance.handled_by_user_id = request.handled_by_user_id
            self.session.add(instance)
            await self.session.commit()
        except Exception as e:
            await self.handle_db_error(e, self.session)
        return instance