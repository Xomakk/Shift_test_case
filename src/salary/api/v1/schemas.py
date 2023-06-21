import uuid
from datetime import datetime

from pydantic import BaseModel


class SalaryBase(BaseModel):
    size: int
    increase_date: datetime

    class Config:
        orm_mode = True


class SalaryEdit(SalaryBase):
    pass


class Salary(SalaryBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
