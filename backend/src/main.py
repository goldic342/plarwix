from contextlib import asynccontextmanager
from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.coder import PickleCoder
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from utils.cache import request_key_builder
from database import get_session
from config import settings
from admin.router import router as admin_router
from admin.service import AdminService
from admin.schemas import SAdminCreate
from auth.router import router as auth_router
from request.router import router as request_router
from subject.router import router as subject_router
from clas.router import router as clas_router
from task.router import router as task_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis = aioredis.Redis(decode_responses=False).from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="/fastapi-cache", coder=PickleCoder, key_builder=request_key_builder)
    async for session in get_session():
        if not await AdminService(session).get_by_login("admin"):
            admin = SAdminCreate(
                first_name="admin",
                last_name="admin",
                login=settings.ADMIN_LOGIN,
                password=settings.ADMIN_PASSWORD,
                is_superuser=True,
            )
            await AdminService(session).add(admin)
        yield
    await redis.flushall()
    await redis.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
@cache(expire=60*60)
def main_page():
    return "Fast api Plarwix"


app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(request_router)
app.include_router(subject_router)
app.include_router(clas_router)
app.include_router(task_router)