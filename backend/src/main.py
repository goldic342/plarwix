from contextlib import asynccontextmanager
from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from database import get_session
from config import settings
from admin.router import router as admin_router
from admin.service import AdminService
from admin.schemas import SAdminCreate
from auth.router import router as auth_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_URL}")
    FastAPICache.init(RedisBackend(redis), prefix="/fastapi-cache")
    async for session in get_session():
        if not await AdminService(session).get_by_login("admin"):
            admin = SAdminCreate(
                first_name="admin",
                last_name="admin",
                login="admin",
                password=settings.ADMIN_PASSWORD,
                is_superuser=True,
            )
            await AdminService(session).add(admin)
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
@cache(expire=60*60)
def main_page():
    return "Fast api Plarwix"


app.include_router(admin_router)
app.include_router(auth_router)
