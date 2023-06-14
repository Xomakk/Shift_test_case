import time
import uuid

from sqlalchemy import create_engine, MetaData, Integer, String, TIMESTAMP, Column, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASS

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# metadata = MetaData()
#
# user = Table(
#     "user",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("email", String, nullable=False),
#     Column("password", String, nullable=False),
#     Column("name", String, default=datetime.utcnow),
#     Column("lastname", String, ForeignKey(role.c.id)),
#     Column("surname", String, nullable=False),
#     Column("salary", Integer, nullable=False),
#     Column("date_of_salary_increase", TIMESTAMP, nullable=False),
# )
#
# token = Table(
#     "role",
#     metadata,
#     Column("id", Integer, index=True, primary_key=True),
#     Column("access_token", String, nullable=False, default=uuid.uuid4),
#     Column("time_create", Float, nullable=False, default=time),
#     Column("user_id", Integer, ForeignKey(user.c.id)),
# )
