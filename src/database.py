from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}".format(
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    db_name=DB_NAME
)
Base = declarative_base()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
