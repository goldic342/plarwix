import uuid
from fastapi import APIRouter, Depends, status
from fastapi.params import Query
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi_cache.decorator import cache

from admin.schemas import (
    SRequestCreate,
    SRequestUpdate,
    SUser,
    SUserCreate,
    SUserUpdate,
)
from auth.depends import get_current_superuser
from auth.service import AuthService
from admin.model import RequestModel, RequestStatus
from utils.cache import get_seconds
from database import get_session
from admin.service import AdminService

router = APIRouter(prefix="/admin")


# user endpoints
@router.post(
    "/add",
    dependencies=[Depends(get_current_superuser)],
    status_code=status.HTTP_201_CREATED,
)
async def add_user(
    user: SUserCreate, session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    user = await AdminService(session).add(user)
    access_token = AuthService.create_access_token({"sub": user.login})
    refresh_token = AuthService.create_refresh_token({"sub": user.login})
    response = JSONResponse({"message": "User was created successfully!"})
    response.headers["Authorization"] = f"Bearer {access_token}"
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return response


@router.delete(
    "/delete/{user_id}",
    dependencies=[Depends(get_current_superuser)],
)
async def delete_user(user_id: str, session: AsyncSession = Depends(get_session)):
    await AdminService(session).delete(user_id)
    return JSONResponse({"message": "User was deleted successfully!"})


@router.put(
    "/update/{user_id}",
    dependencies=[Depends(get_current_superuser)],
    response_model=SUser,
)
async def update_user(
    user_id: str, user: SUserUpdate, session: AsyncSession = Depends(get_session)
):
    return await AdminService(session).update(user_id, **user.model_dump())


@router.get(
    "/all", dependencies=[Depends(get_current_superuser)], response_model=list[SUser]
)
async def get_all_users(session: AsyncSession = Depends(get_session)) -> list[SUser]:
    return await AdminService(session).get_all()


@router.get(
    "/id/{user_id}",
    dependencies=[Depends(get_current_superuser)],
    response_model=SUser,
)
async def get_user_by_id(
    user_id: str, session: AsyncSession = Depends(get_session)
) -> SUser:
    result = await AdminService(session).get_by_id(user_id)
    return result


@router.get(
    "/login/{login}",
    dependencies=[Depends(get_current_superuser)],
    response_model=SUser,
)
async def get_user_by_login(
    login: str, session: AsyncSession = Depends(get_session)
) -> SUser:
    result = await AdminService(session).get_by_login(login)
    return result

# request endpoints
@router.post("/request/add", response_model=RequestModel)
async def add_request(
    request: SRequestCreate, session: AsyncSession = Depends(get_session)
) -> RequestModel:
    return await AdminService(session).add_request(request)


@router.put("/request/update/{request_id}", response_model=RequestModel)
async def update_request(
    request_id: str,
    request: SRequestUpdate,
    session: AsyncSession = Depends(get_session),
) -> RequestModel:
    return await AdminService(session).update_request(request_id, request)


@router.get(
    "/request/all",
    dependencies=[Depends(get_current_superuser)],
    response_model=list[RequestModel],
)
@cache(expire=get_seconds(minutes=5))
async def get_all_requests(
    filter_by_status: RequestStatus | None = None,
    filter_by_user_id: uuid.UUID | None = None,
    session: AsyncSession = Depends(get_session),
) -> list[RequestModel]:
    result = await AdminService(session).get_all_requests(
        filter_by_status, filter_by_user_id
    )
    return result
