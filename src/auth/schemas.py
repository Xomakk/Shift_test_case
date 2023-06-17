from pydantic import BaseModel, EmailStr


class TokenBase(BaseModel):
    access_token: str
    time_create: float


class TokenCreate(TokenBase):
    pass


class Token(TokenBase):
    id: int
    user_id: int

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
    id: int

    class Config:
        orm_mode = True
