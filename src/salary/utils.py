import uuid

from fastapi import HTTPException, status
from sqlalchemy import select, UUID, Column
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from src.salary import models, schemas


async def create_salary(user_id: Column[uuid.UUID], db: AsyncSession) -> models.Salary:
    db_salary = models.Salary(
        size=0,
        user_id=user_id,
        increase_date=None
    )
    db.add(db_salary)
    await db.commit()
    await db.refresh(db_salary)
    return db_salary


async def get_salary_by_user_id(user_id: uuid.UUID, db: AsyncSession) -> models.Salary:
    query = select(models.Salary).where(models.Salary.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().one()


async def edit_user_salary(user_id: uuid.UUID, salary_data: schemas.SalaryEdit, db: AsyncSession) -> models.Salary:
    salary = await get_salary_by_user_id(user_id, db)
    try:
        salary.size = salary_data.size
        salary.increase_date = salary_data.increase_date
        db.add(salary)
        await db.commit()
    except DBAPIError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The increase_date is in the wrong format"
        )
    return salary
