import uuid
from typing import Union

from fastapi import HTTPException, status
from sqlalchemy import select, Column
from sqlalchemy.exc import DBAPIError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.salary import models, schemas


async def get_salary_by_user_id(user_id: uuid.UUID, db: AsyncSession) -> models.Salary:
    try:
        query = select(models.Salary).where(models.Salary.user_id == user_id)
        result = await db.execute(query)
        return result.scalars().one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("The salary of the user with the "
                    "specified ID was not found. Perhaps "
                    "the salary for the specified user does "
                    "not exist or the ID is incorrect")
        )


async def edit_user_salary_by_id(salary_data: schemas.SalaryEdit, db: AsyncSession) -> models.Salary:
    salary = await get_salary_by_user_id(salary_data.user_id, db)
    print(salary_data.increase_date)
    salary.size = salary_data.size
    salary.increase_date = salary_data.increase_date
    db.add(salary)
    await db.commit()
    return salary


async def create_user_salary_by_id(
        db: AsyncSession,
        data: Union[schemas.SalaryCreate, None] = None,
        user_id: Union[uuid.UUID, None] = None
) -> models.Salary:
    try:
        salary = await get_salary_by_user_id(data.user_id, db)
    except AttributeError:
        salary = None
    except HTTPException:
        salary = None

    if salary:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The salary of the user with the specified id already exists. Try editing it"
        )

    if data:
        db_salary = models.Salary(
            size=data.size,
            user_id=data.user_id,
            increase_date=data.increase_date
        )
    else:
        db_salary = models.Salary(
            size=0,
            user_id=user_id,
            increase_date=None
        )

    db.add(db_salary)
    await db.commit()
    await db.refresh(db_salary)
    return db_salary


async def delete_user_salary_by_id(salary_data: schemas.SalaryDelete, db: AsyncSession) -> str:
    salary = await get_salary_by_user_id(salary_data.user_id, db)
    await db.delete(salary)
    await db.commit()
    return "success"
