import uuid
from datetime import datetime

from pydantic import BaseModel


class SalaryBase(BaseModel):
    user_id: uuid.UUID

    class Config:
        orm_mode = True


class SalaryEdit(SalaryBase):
    size: int
    increase_date: datetime


class SalaryCreate(SalaryEdit):
    pass


class SalaryGet(SalaryBase):
    pass


class SalaryDelete(SalaryBase):
    pass


class Salary(SalaryBase):
    id: uuid.UUID
    size: int
    increase_date: datetime

    class Config:
        orm_mode = True
