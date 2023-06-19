from pydantic import BaseModel, EmailStr
from sqlalchemy import UUID


class TokenBase(BaseModel):
    access_token: UUID
    time_create: float


class TokenCreate(TokenBase):
    pass


class Token(TokenBase):
    id: UUID
    user_id: UUID

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    name: str
    lastname: str
    surname: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID

    class Config:
        orm_mode = True
