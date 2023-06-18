from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.salary import models as salary_model
from src.auth import schemas
from src.auth.utils import create_token, get_user_by_email, create_user, get_current_user, oauth2_scheme, check_token, \
    get_token
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


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_email(form_data.username, db)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    if not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )

    access_token = await create_token(db, user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user", response_model=schemas.User, dependencies=[Depends(check_token)])
async def get_user(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@router.post("/logout", dependencies=[Depends(check_token)])
async def logout(access_token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_async_session)):
    token = await get_token(access_token, db)
    await db.delete(token)
    await db.commit()

    return HTTPException(
        status_code=200,
        detail="Logout success"
    )
