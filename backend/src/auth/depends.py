from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, Request

from admin.model import UserBase
from admin.service import AdminService
from auth.service import AuthService
from database import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> UserBase:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = AuthService.verify_token(token, credentials_exception)
    if payload is None:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise credentials_exception
        payload = AuthService.verify_token(refresh_token, credentials_exception)
        if payload is None:
            raise credentials_exception
    login = payload.get("sub")

    if login is None:
        raise credentials_exception
    user = await AdminService(session).get_by_login(login)
    if user is None:
        raise credentials_exception
    return user

async def get_current_superuser(
    user= Depends(get_current_user)
):
    if not user.is_superuser:
        raise HTTPException(
            status_code=403, detail='Superuser access required')
    return user
