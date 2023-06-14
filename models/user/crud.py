import hashlib
import uuid
from time import time

from sqlalchemy.orm import Session

from models.user import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.User).offset(offset).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashlib.sha256(user.password)
    db_user = models.User(
        email=user.email,
        password=hashed_password,
        name=user.name,
        lastname=user.lastname,
        surname=user.surname,
        salary=user.salary
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_token(db: Session, user_id: int):
    db_token = models.Token(
        access_token=uuid.uuid4(),
        time_create=time(),
        user_id=user_id
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token
