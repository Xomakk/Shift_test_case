import uuid
from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import schemas, models, utils
from src.database import get_async_session
from src.salary.utils import create_user_salary_by_id

router = APIRouter(
    prefix="/auth",
    tags=["Authenticate"]
)


@router.post("/create_user", response_model=schemas.User)
async def create_user(user_data: schemas.UserCreate,
                      db: AsyncSession = Depends(get_async_session)) -> models.User:
    """
        Creating a new user.
        Permissions: All
    """
    user = await utils.get_user_by_email(user_data.email, db)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered"
        )
    new_user = await utils.create_user(user_data, db)
    await create_user_salary_by_id(db, user_id=new_user.id)
    return new_user


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_async_session)) -> dict[str, Union[uuid.UUID, str]]:
    """
        User authorization and access token issuance.
        Permissions: All
    """
    user = await utils.get_user_by_email(form_data.username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if not await utils.verify_password(user.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    access_token = await utils.create_token(db, user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile/my", response_model=schemas.User, dependencies=[Depends(utils.check_token)])
async def get_current_user(current_user: schemas.User = Depends(utils.get_current_user)) -> schemas.User:
    """
        Getting data about the current user.
        Permissions: authorized user
    """
    return current_user


@router.get(
    "/profile/user",
    response_model=schemas.User,
    dependencies=[Depends(utils.check_token), Depends(utils.check_permission)]
)
async def get_user_by_id(user_id: uuid.UUID, db: AsyncSession = Depends(get_async_session)) -> schemas.User:
    """
        Getting data about the user by id.
        Permissions: only admin
    """
    return await utils.get_user_by_id(user_id, db)


@router.put(
    "/profile/edit",
    response_model=schemas.User,
    dependencies=[Depends(utils.check_token), Depends(utils.check_permission)]
)
async def edit_user(
        data: schemas.UserEdit,
        db: AsyncSession = Depends(get_async_session)
) -> schemas.UserEdit:
    """
        Editing user data by id.
        Permissions: only admin
    """
    return await utils.edit_user_data_by_id(data, db)


@router.get("/logout", dependencies=[Depends(utils.check_token)])
async def logout(access_token: Annotated[str, Depends(utils.oauth2_scheme)],
                 db: AsyncSession = Depends(get_async_session)) -> None:
    """
        User logging out and deleting the access token.
        Permissions: authorized user
    """
    token = await utils.get_token(access_token, db)
    await db.delete(token)
    await db.commit()

    return
