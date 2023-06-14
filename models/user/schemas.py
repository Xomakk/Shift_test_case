from pydantic import BaseModel


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
    email: str
    name: str
    lastname: str
    surname: str
    salary: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    token: list[Token] = []

    class Config:
        orm_mode = True
