import uuid
from pydantic import BaseModel

from request.model import RequestStatus


class SRequestCreate(BaseModel):
    message: str


class SRequestUpdate(BaseModel):
    status: RequestStatus

class SRequestUpdateByUser(SRequestUpdate):
    handled_by_user_id: uuid.UUID = None