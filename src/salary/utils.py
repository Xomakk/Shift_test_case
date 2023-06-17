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
