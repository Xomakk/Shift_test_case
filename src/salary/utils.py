from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from src.salary import models


async def create_salary(user_id: int, db: AsyncSession):
    db_salary = models.Salary(
        size=0,
        user_id=user_id,
        increase_date=None
    )
    db.add(db_salary)
    await db.commit()
    await db.refresh(db_salary)
    return db_salary


async def get_salary_by_user_id(user_id: int, db: AsyncSession):
    query = select(models.Salary).where(models.Salary.user_id == user_id)
    result = await db.execute(query)
    salary = result.scalars().first()
    return salary


async def edit_user_salary(user_id: int, salary_data, db: AsyncSession):
    salary = await get_salary_by_user_id(user_id, db)
    try:
        salary.size = salary_data.size
        salary.increase_date = salary_data.increase_date
        db.add(salary)
        await db.commit()
    except DBAPIError:
        raise HTTPException(
            status_code=400,
            detail="The increase_date is in the wrong format"
        )
    return salary
