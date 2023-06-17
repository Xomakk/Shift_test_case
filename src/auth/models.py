import hashlib
import uuid
from time import time
from sqlalchemy import Integer, String, TIMESTAMP, Column, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, index=True, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    token = relationship("Token", back_populates="user", uselist=False)
    salary = relationship("Salary", back_populates="user", uselist=False)

    def verify_password(self, input_password):
        return self.password == hashlib.sha256(input_password.encode('utf-8')).hexdigest()


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, index=True, primary_key=True)
    access_token = Column(String, nullable=False, default=lambda: str(uuid.uuid4), index=True)
    time_create = Column(Integer, nullable=False, default=lambda: int(time()))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

    user = relationship("User")
