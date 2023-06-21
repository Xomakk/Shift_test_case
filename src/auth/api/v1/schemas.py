import uuid

from pydantic import BaseModel, EmailStr


class TokenBase(BaseModel):
    access_token: uuid.UUID
    time_create: float


class TokenCreate(TokenBase):
    pass


class Token(TokenBase):
    id: uuid.UUID
    user_id: uuid.UUID

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
    id: uuid.UUID

    class Config:
        orm_mode = True
