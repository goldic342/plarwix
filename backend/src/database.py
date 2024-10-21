from datetime import datetime
import uuid
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


from config import get_db_url


DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

uuid_id = Field(default_factory=uuid.uuid4, primary_key=True)
created_at = Field(default_factory=datetime.now, sa_column_kwargs={'server_default': func.now()})
edited_at = Field(default_factory=datetime.now,  sa_column_kwargs={'server_default': func.now(), 'onupdate': func.now()})

async def get_session() -> AsyncSession: # type: ignore
    async with async_session_maker() as session:
        yield session

class Base(SQLModel):
    __abstract__ = True
    
    created_at: datetime | None =  created_at
    edited_at: datetime | None = edited_at