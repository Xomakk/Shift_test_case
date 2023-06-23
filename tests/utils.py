from httpx import AsyncClient
from sqlalchemy import select

from src.auth import models
from tests.conftest import async_session_maker


async def delete_user(email) -> None:
    async with async_session_maker() as session:
        query = select(models.User).where(models.User.email == email)
        result = await session.execute(query)
        user = result.scalars().first()
        if user:
            await session.delete(user)
