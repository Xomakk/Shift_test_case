import hashlib
import uuid
from time import time
from typing import Annotated, Union

import sqlalchemy.exc
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, Column, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth import models
from src.auth import schemas
from src import config as cfg
from src.database import get_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def create_token(db: AsyncSession, user: models.User) -> Column[uuid.UUID]:
    access_token = uuid.uuid4()
    token = models.Token(
        access_token=access_token,
        user_id=user.id
    )
    db.add(token)
    await db.commit()
    await db.refresh(token)
    return token.access_token


async def create_user(data: schemas.UserCreate, db: AsyncSession) -> models.User:
    hashed_password = hashlib.sha256(data.password.encode('utf-8')).hexdigest()
    db_user = models.User(
        email=data.email,
        password=hashed_password,
        name=data.name,
        lastname=data.lastname,
        patronymic=data.patronymic,
        is_admin=data.is_admin
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_email(email: str, db: AsyncSession) -> Union[models.User, None]:
    try:
        query = select(models.User).where(models.User.email == email).options(
            selectinload(models.User.token), selectinload(models.User.salary)
        )
        result = await db.execute(query)
        return result.scalars().one()
    except sqlalchemy.exc.NoResultFound:
        return None


async def get_user_by_id(id: uuid.UUID, db: AsyncSession) -> Union[models.User, None]:
    try:
        query = select(models.User).where(models.User.id == id).options(
            selectinload(models.User.token), selectinload(models.User.salary)
        )
        result = await db.execute(query)
        return result.scalars().one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with the specified id was not found",
        )


async def get_token(access_token: str, db: AsyncSession) -> models.Token:
    try:
        query = select(models.Token).where(models.Token.access_token == access_token).options(
            selectinload(models.Token.user)
        )
        result = await db.execute(query)
        return result.scalars().one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is expired. You need re-log in",
        )


async def get_current_user(
        access_token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_async_session)
) -> models.User:
    token = await get_token(access_token, db)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return token.user


async def revoke_token(token: models.Token, db: AsyncSession) -> None:
    await db.delete(token)
    await db.commit()


async def check_token(access_token: Annotated[str, Depends(oauth2_scheme)],
                      db: AsyncSession = Depends(get_async_session)) -> None:
    token = await get_token(access_token, db)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    if token.time_create < int(time()) - int(cfg.TOKEN_LIFETIME):
        await revoke_token(token, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is expired. You need re-log in",
        )


async def verify_password(user_password: Column[str], input_password: str) -> ColumnElement[bool]:
    return user_password == hashlib.sha256(input_password.encode('utf-8')).hexdigest()


def check_permission(current_user: schemas.User = Depends(get_current_user)) -> None:
    if current_user.is_admin:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have the permissions to perform this operation",
    )


async def edit_user_data_by_id(data: schemas.UserEdit, db: AsyncSession) -> models.User:
    user = await get_user_by_id(data.id, db)
    if data.name:
        user.name = data.name
    if data.lastname:
        user.lastname = data.lastname
    if data.patronymic:
        user.patronymic = data.patronymic
    if data.is_admin:
        user.is_admin = data.is_admin
    db.add(user)
    await db.commit()
    return user
