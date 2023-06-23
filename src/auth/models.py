import uuid
from time import time
from sqlalchemy import Integer, String, Column, ForeignKey, UUID, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID, index=True, primary_key=True, default=uuid.uuid4)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    token = relationship("Token", back_populates="user")
    salary = relationship("Salary", back_populates="user", uselist=False)


class Token(Base):
    __tablename__ = "token"

    id = Column(UUID, index=True, primary_key=True, default=uuid.uuid4)
    access_token = Column(UUID, nullable=False, default=lambda: uuid.uuid4, index=True)
    time_create = Column(Integer, nullable=False, default=lambda: int(time()))
    user_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"))

    user = relationship("User")
