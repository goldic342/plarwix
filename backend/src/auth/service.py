from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
import jwt

from admin.service import AdminService
from config import settings



class AuthService:

    def __init__(self, session: AsyncSession = None) -> None:
        self.session = session

    async def authenticate_user(self, login: str, password: str):
        user = await AdminService(self.session).get_by_login(login)
        if not AdminService.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        return user


    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict):
        to_encode = data.copy()
        expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str, exception: HTTPException):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            exception.detail = "Token is invalid"
            raise exception