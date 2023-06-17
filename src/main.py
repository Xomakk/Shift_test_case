from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.salary.router import router as salary_router

API_VERSION = "api"

app = FastAPI(
    title="Actual salary"
)

app.include_router(auth_router, prefix=f"/{API_VERSION}")
app.include_router(salary_router, prefix=f"/{API_VERSION}")
