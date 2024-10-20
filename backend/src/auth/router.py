from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.depends import get_current_user
from auth.schemas import SAdminLogin
from auth.service import AuthService
from admin.model import UserBase
from database import get_session


router = APIRouter(prefix='/auth')

@router.post("/login")
async def login_user(
    user: SAdminLogin, session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    user = await AuthService(session).authenticate_user(**user.model_dump())
    access_token = AuthService.create_access_token({"sub": user.login})
    refresh_token = AuthService.create_refresh_token({"sub": user.login})
    response = JSONResponse({"message": "Login successful!"})
    response.headers["Authorization"] = f"Bearer {access_token}"
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
    return response



@router.get("/me")
async def get_me(
    current_user: UserBase = Depends(get_current_user),
) -> UserBase:
    return current_user