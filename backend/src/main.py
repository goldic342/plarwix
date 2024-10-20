from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import get_session
from config import settings
from admin.router import router as admin_router
from admin.service import AdminService
from admin.schemas import SAdminCreate
from auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async for session in get_session():
        if not await AdminService(session).get_by_login('admin'):
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
def main_page():
    return "Fast api test"


app.include_router(admin_router)
app.include_router(auth_router)
