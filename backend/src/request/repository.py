import uuid
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import select

from request.model import RequestModel, RequestStatus
from core.repository import BaseRepository


class RequestRepository(BaseRepository):
    model = RequestModel

    def error_message(self, e: Exception) -> str | Exception:
        if isinstance(e, IntegrityError):
            return "The request is already exists"
        elif isinstance(e, NoResultFound):
            return "The request wasn't found"
        else:
            return e

    async def get_all(
        self,
        filter_by_status: RequestStatus | None = None,
        filter_by_user_id: uuid.UUID | None = None,
    ) -> list[RequestModel]:
        try:
            query = select(RequestModel)
            if filter_by_status:
                query = query.filter_by(status=filter_by_status)
            if filter_by_user_id:
                query = query.filter_by(handled_by_user_id=filter_by_user_id)
            result = await self.session.exec(query)
            return result.all()
        except Exception as e:
            await self.handle_db_error(e, self.session)
    