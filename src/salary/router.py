from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import get_user_by_id, check_token, get_token
from src.database import get_async_session
from src.salary import models, schemas

router = APIRouter(
    prefix="/salary",
    tags=["Salary"]
)


@router.post("/edit", response_model=schemas.SalaryEdit)
async def edit_salary_for_current_user(request: Request, data: schemas.SalaryEdit,
                                       db: AsyncSession = Depends(get_async_session)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=400,
            detail="You are not logged in."
        )

    token = await get_token(access_token, db)
    if not await check_token(token, db):
        raise HTTPException(
            status_code=400,
            detail="access_token is expired. You need re-log in."
        )

    user_id = token.user.id
    query = select(models.Salary).where(models.Salary.user_id == user_id)
    result = await db.execute(query)
    salary = result.scalars().first()
    try:
        salary.size = data.size
        salary.increase_date = data.increase_date
        db.add(salary)
        await db.commit()
        return salary
    except DBAPIError:
        raise HTTPException(
            status_code=400,
            detail="The increase_date is in the wrong format"
        )


@router.get("/get", response_model=schemas.Salary)
async def get_current_user_salary(request: Request, db: AsyncSession = Depends(get_async_session)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=400,
            detail="You are not logged in."
        )

    token = await get_token(access_token, db)
    if not await check_token(token, db):
        raise HTTPException(
            status_code=400,
            detail="access_token is expired. You need re-log in."
        )
    user_id = token.user.id
    user = await get_user_by_id(user_id, db)
    return user.salary
