from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import get_user_by_id, check_token, get_token, get_current_user
from src.database import get_async_session
from src.salary import models, schemas
from src.auth import schemas as user_schemas
from src.salary.utils import edit_user_salary, get_salary_by_user_id

router = APIRouter(
    prefix="/salary",
    tags=["Salary"]
)


@router.post("/edit", response_model=schemas.SalaryEdit, dependencies=[Depends(check_token)])
async def edit_salary_for_current_user(
        data: schemas.SalaryEdit,
        current_user: user_schemas.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session)
):
    edited_salary = await edit_user_salary(current_user.id, data, db)
    return edited_salary


@router.get("/get", response_model=schemas.Salary, dependencies=[Depends(check_token)])
async def get_current_user_salary(
        current_user: user_schemas.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session)
):
    salary = await get_salary_by_user_id(current_user.id, db)
    return salary
