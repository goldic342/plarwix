import uuid
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.depends import get_current_superuser
from admin.model import UserBase
from request.service import RequestService
from database import get_session
from request.model import RequestModel, RequestStatus
from request.schema import SRequestCreate, SRequestUpdate, SRequestUpdateByUser
from utils.cache import get_seconds


router = APIRouter(prefix="/request")

@router.post("/add", response_model=RequestModel)
async def add_request(
    request: SRequestCreate, session: AsyncSession = Depends(get_session)
) -> RequestModel:
    return await RequestService(session).add(request)


@router.put("/update/{request_id}", response_model=RequestModel)
async def update_request(
    request_id: uuid.UUID,
    request: SRequestUpdate,
    session: AsyncSession = Depends(get_session),
    user: UserBase = Depends(get_current_superuser)
) -> RequestModel:
    request = SRequestUpdateByUser(status=request.status, handled_by_user_id=user.id)
    return await RequestService(session).update(request_id, request)


@router.get(
    "/all",
    dependencies=[Depends(get_current_superuser)],
    response_model=list[RequestModel],
)
@cache(expire=get_seconds(minutes=5))
async def get_all_requests(
    filter_by_status: RequestStatus | None = None,
    filter_by_user_id: uuid.UUID | None = None,
    session: AsyncSession = Depends(get_session),
) -> list[RequestModel]:
    result = await RequestService(session).get_all(
        filter_by_status, filter_by_user_id
    )
    return result