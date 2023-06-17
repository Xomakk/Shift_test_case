import hashlib
import uuid
from time import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth import models
from src.auth.schemas import UserCreate
from src.config import TOKEN_LIFETIME


async def create_token(db: AsyncSession, user: models.User):
    if user.token:
        await db.delete(user.token)
    access_token = str(uuid.uuid4())
    token = models.Token(
        access_token=access_token,
        user_id=user.id
    )
    db.add(token)
    await db.commit()
    await db.refresh(token)
    return access_token


async def create_user(data: UserCreate, db: AsyncSession):
    hashed_password = hashlib.sha256(data.password.encode('utf-8')).hexdigest()
    db_user = models.User(
        email=data.email,
        password=hashed_password,
        name=data.name,
        lastname=data.lastname,
        surname=data.surname,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_email(email: str, db: AsyncSession):
    query = select(models.User).where(models.User.email == email).options(
        selectinload(models.User.token), selectinload(models.User.salary)
    )
    result = await db.execute(query)
    return result.scalars().first()


async def get_user_by_id(id: int, db: AsyncSession):
    query = select(models.User).where(models.User.id == id).options(
        selectinload(models.User.token), selectinload(models.User.salary)
    )
    result = await db.execute(query)
    return result.scalars().first()


async def get_token(access_token: str, db: AsyncSession):
    query = select(models.Token).where(models.Token.access_token == access_token).options(
        selectinload(models.Token.user)
    )
    result = await db.execute(query)
    return result.scalars().first()


async def check_token(token, db: AsyncSession):
    if not token:
        return False

    if token.time_create < int(time()) - int(TOKEN_LIFETIME):
        await db.delete(token)
        await db.commit()
        return False

    return True

# def check_permission(func):
#     def _wrapper(*args, db: AsyncSession = Depends(get_async_session), **kwargs):
#         print("***********", kwargs)
#         access_token = kwargs["request"].cookies.get("access_token")
#         if not access_token:
#             raise HTTPException(
#                 status_code=400,
#                 detail="You are not logged in."
#             )
#
#         token = await get_token(access_token, db)
#         if not await check_token(token, db):
#             raise HTTPException(
#                 status_code=400,
#                 detail="access_token is expired. You need re-log in."
#             )
#         return func(*args, **kwargs, token=token)
#
#     return _wrapper
