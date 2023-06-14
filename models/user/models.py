import uuid
from time import time
from datetime import datetime, timedelta
from sqlalchemy import Integer, String, TIMESTAMP, Column, ForeignKey, Float
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, index=True, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    date_of_salary_increase = Column(TIMESTAMP, default=lambda: datetime.utcnow() + timedelta(days=90))

    token = relationship("Token", back_populates="token")


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, index=True, primary_key=True)
    access_token = Column(String, nullable=False, default=uuid.uuid4)
    time_create = Column(Float, nullable=False, default=time)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="user")
