import hashlib
import uuid
from time import time
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, Column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth import models
from src.auth.schemas import UserCreate
from src import config as cfg
from src.database import get_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def create_token(db: AsyncSession, user: models.User) -> Column[uuid.UUID]:
    if user.token:
        await db.delete(user.token)
    access_token = uuid.uuid4()
    token = models.Token(
        access_token=access_token,
        user_id=user.id
    )
    db.add(token)
    await db.commit()
    await db.refresh(token)
    return token.access_token


async def create_user(data: UserCreate, db: AsyncSession) -> models.User:
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


async def get_user_by_email(email: str, db: AsyncSession) -> models.User:
    query = select(models.User).where(models.User.email == email).options(
        selectinload(models.User.token), selectinload(models.User.salary)
    )
    result = await db.execute(query)
    return result.scalars().one()


async def get_user_by_id(id: int, db: AsyncSession) -> models.User:
    query = select(models.User).where(models.User.id == id).options(
        selectinload(models.User.token), selectinload(models.User.salary)
    )
    result = await db.execute(query)
    return result.scalars().one()


async def get_token(access_token: str, db: AsyncSession) -> models.Token:
    query = select(models.Token).where(models.Token.access_token == access_token).options(
        selectinload(models.Token.user)
    )
    result = await db.execute(query)
    return result.scalars().one()


async def get_current_user(
        access_token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_async_session)
) -> models.User:
    token = await get_token(access_token, db)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token.user


async def check_token(access_token: Annotated[str, Depends(oauth2_scheme)],
                      db: AsyncSession = Depends(get_async_session)) -> None:
    token = await get_token(access_token, db)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if token.time_create < int(time()) - int(cfg.TOKEN_LIFETIME):
        await db.delete(token)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is expired. You need re-log in.",
            headers={"WWW-Authenticate": "Bearer"}
        )
