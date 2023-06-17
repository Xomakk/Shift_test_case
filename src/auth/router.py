from typing import Annotated

from fastapi import APIRouter, Depends, Form, Response, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import TOKEN_LIFETIME
from src.salary import models as salary_model
from src.auth import schemas
from src.auth.utils import create_token, get_user_by_email, create_user
from src.database import get_async_session
from src.salary.utils import create_salary

router = APIRouter(
    prefix="/auth",
    tags=["Authenticate"]
)


@router.post("/create_user", response_model=schemas.User)
async def create_new_user(user_data: schemas.UserCreate, db: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_email(user_data.email, db)
    if user:
        raise HTTPException(
            status_code=400,
            detail="This email is already registered"
        )
    new_user = await create_user(user_data, db)
    await create_salary(new_user.id, db)
    return new_user


@router.post("/login", response_model=schemas.User)
async def login(response: Response, email: Annotated[EmailStr, Form()], password: Annotated[str, Form()],
                db: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
    if not user.verify_password(password):
        raise HTTPException(
            status_code=400,
            detail="Password error"
        )

    access_token = await create_token(db, user)
    response.set_cookie(key="access_token", value=access_token, max_age=TOKEN_LIFETIME)
    return user


@router.post("/logout")
async def logout(response: Response, db: AsyncSession = Depends(get_async_session)):
    response.delete_cookie("access_token")
    return HTTPException(
        status_code=200,
        detail="Logout success"
    )
