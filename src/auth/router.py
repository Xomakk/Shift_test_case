import uuid
from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import verify_password
from src.salary import models as salary_model
from src.auth import schemas, models
from src.auth import utils
from src.database import get_async_session
from src.salary.utils import create_salary

router = APIRouter(
    prefix="/auth",
    tags=["Authenticate"]
)


@router.post("/create_user", response_model=schemas.User)
async def create_new_user(user_data: schemas.UserCreate,
                          db: AsyncSession = Depends(get_async_session)) -> models.User:
    user = await utils.get_user_by_email(user_data.email, db)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered"
        )
    new_user = await utils.create_user(user_data, db)
    await create_salary(new_user.id, db)
    return new_user


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_async_session)) -> dict[str, Union[uuid.UUID, str]]:
    user = await utils.get_user_by_email(form_data.username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if not await verify_password(user.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    access_token = await utils.create_token(db, user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user", response_model=schemas.User, dependencies=[Depends(utils.check_token)])
async def get_user(current_user: schemas.User = Depends(utils.get_current_user)) -> schemas.User:
    return current_user


@router.get("/logout", dependencies=[Depends(utils.check_token)])
async def logout(access_token: Annotated[str, Depends(utils.oauth2_scheme)],
                 db: AsyncSession = Depends(get_async_session)) -> None:
    token = await utils.get_token(access_token, db)
    await db.delete(token)
    await db.commit()

    return
