import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import get_current_user, check_permission
from src.database import get_async_session
from src.salary import models, schemas
from src.auth import schemas as user_schemas
from src.salary import utils

router = APIRouter(
    prefix="/salary",
    tags=["Salary"]
)


@router.put("/edit", response_model=schemas.SalaryEdit, dependencies=[Depends(check_permission)])
async def edit_salary(
        data: schemas.SalaryEdit,
        db: AsyncSession = Depends(get_async_session)
) -> models.Salary:
    """
        Editing the user's salary by the administrator by the transmitted id.
        Permissions: admin only
    """
    return await utils.edit_user_salary_by_id(data, db)


@router.delete("/delete", dependencies=[Depends(check_permission)])
async def delete_salary(
        data: schemas.SalaryDelete,
        db: AsyncSession = Depends(get_async_session)
):
    """
        Deleting a salary by user id.
        Permissions: admin only
    """
    return await utils.delete_user_salary_by_id(data, db)


@router.post("/create", dependencies=[Depends(check_permission)])
async def create_salary(
        data: schemas.SalaryCreate,
        db: AsyncSession = Depends(get_async_session)
):
    """
        Deleting a salary by user id.
        Permissions: admin only
    """
    return await utils.create_user_salary_by_id(db, data=data)


@router.get("/get", response_model=schemas.Salary, dependencies=[Depends(check_permission)])
async def get_user_salary_by_id(
        user_id: uuid.UUID,
        db: AsyncSession = Depends(get_async_session)
) -> models.Salary:
    """
        Receiving the user's salary.
        Permissions: admin only
    """
    return await utils.get_salary_by_user_id(user_id, db)


@router.get("/my", response_model=schemas.Salary)
async def get_current_user_salary(
        current_user: user_schemas.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session)
) -> models.Salary:
    """
        Getting the current user's salary.
        Permissions: authorized user
    """
    return await utils.get_salary_by_user_id(current_user.id, db)
