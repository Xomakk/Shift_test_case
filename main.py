from fastapi import FastAPI

import database
from models.user import crud, models, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def hello():
    return "Hello"
