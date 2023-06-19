from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import UUID, Column


class SalaryBase(BaseModel):
    size: Column[int]
    increase_date: Column[datetime]

    class Config:
        orm_mode = True


class SalaryEdit(SalaryBase):
    pass


class Salary(SalaryBase):
    id: UUID

    class Config:
        orm_mode = True
