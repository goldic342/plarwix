from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from admin.schemas import SRequestCreate, SRequestUpdate, SUserCreate, SUserUpdate
from auth.depends import get_current_superuser
from auth.service import AuthService
from admin.model import RequestModel, UserBase
from database import get_session
from admin.service import AdminService

router = APIRouter(prefix="/admin")


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
    "/update", dependencies=[Depends(get_current_superuser)], response_model=UserBase
)
async def update_user(user: SUserUpdate, session: AsyncSession = Depends(get_session)):
    return await AdminService(session).update(**user.model_dump())


@router.get(
    "/all", dependencies=[Depends(get_current_superuser)], response_model=list[UserBase]
)
async def get_all_users(session: AsyncSession = Depends(get_session)) -> list[UserBase]:
    return await AdminService(session).get_all()


@router.get(
    "/request",
    dependencies=[Depends(get_current_superuser)],
    response_model=list[RequestModel],
)
async def get_all_request(
    session: AsyncSession = Depends(get_session),
) -> list[RequestModel]:
    return await AdminService(session).get_all_requests()


@router.post("/request/add", response_model=RequestModel)
async def get_all_request(
    request: SRequestCreate, session: AsyncSession = Depends(get_session)
) -> RequestModel:
    return await AdminService(session).add_request(request)


@router.put("/request/update", response_model=RequestModel)
async def update_request(
    request: SRequestUpdate, session: AsyncSession = Depends(get_session)
) -> RequestModel:
    return await AdminService(session).request_update(request)


@router.get(
    "/id/{user_id}",
    dependencies=[Depends(get_current_superuser)],
    response_model=UserBase,
)
async def get_user_by_id(
    user_id: str, session: AsyncSession = Depends(get_session)
) -> UserBase:
    result = await AdminService(session).get_by_id(user_id)
    return result


@router.get(
    "/login/{login}",
    dependencies=[Depends(get_current_superuser)],
    response_model=UserBase,
)
async def get_user_by_login(
    login: str, session: AsyncSession = Depends(get_session)
) -> UserBase:
    result = await AdminService(session).get_by_login(login)
    return result
