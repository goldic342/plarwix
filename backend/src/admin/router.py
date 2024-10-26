import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from admin.schemas import (
    SUser,
    SUserCreate,
    SUserUpdate,
)
from auth.depends import get_current_superuser
from auth.service import AuthService
from task.service import TaskService
from user_clas.service import UserClasService
from user_subject.service import UserSubjectService
from database import get_session
from config import settings
from admin.service import AdminService
from user_subject.router import router as subject_user_router
from user_clas.router import router as clas_user_router

router = APIRouter(prefix="/admin")

if settings.ENVIRONMENT != "test":
    router.dependencies = [Depends(get_current_superuser)]

router.include_router(subject_user_router)
router.include_router(clas_user_router)

@router.post(
    "/add",
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
)
async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    await AdminService(session).delete(user_id)
    await UserSubjectService.delete_by_user_id(user_id)
    await UserClasService.delete_by_user_id(user_id)
    await TaskService.delete_tasks_by_user_id(user_id)
    return JSONResponse({"message": "User was deleted successfully!"})


@router.put(
    "/update/{user_id}",
    response_model=SUser,
)
async def update_user(
    user_id: uuid.UUID, user: SUserUpdate, session: AsyncSession = Depends(get_session)
):
    return await AdminService(session).update(user_id, **user.model_dump())


@router.get("/all", response_model=list[SUser])
async def get_all_users(session: AsyncSession = Depends(get_session)) -> list[SUser]:
    return await AdminService(session).get_all()


@router.get(
    "/id/{user_id}",
    response_model=SUser,
)
async def get_user_by_id(
    user_id: uuid.UUID, session: AsyncSession = Depends(get_session)
) -> SUser:
    result = await AdminService(session).get_by_id(user_id)
    return result


@router.get(
    "/login/{login}",
    response_model=SUser,
)
async def get_user_by_login(
    login: str, session: AsyncSession = Depends(get_session)
) -> SUser:
    result = await AdminService(session).get_by_login(login)
    return result
