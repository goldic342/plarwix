import uuid
from request.model import RequestModel, RequestStatus
from request.repository import RequestRepository
from core.service import BaseService


class RequestService(BaseService):
    repository = RequestRepository

    async def get_all(
        self,
        filter_by_status: RequestStatus | None = None,
        filter_by_user_id: uuid.UUID | None = None,
    ) -> list[RequestModel]:
        return await self.repository(self.session).get_all(filter_by_status, filter_by_user_id)
