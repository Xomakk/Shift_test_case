from fastapi import FastAPI, Depends

from src.auth.api.v1.router import router as auth_router
from src.auth.utils import check_token
from src.salary.api.v1.router import router as salary_router

API_VERSION_v1 = "api/v1"

app = FastAPI(
    title="Actual salary"
)

app.include_router(auth_router, prefix=f"/{API_VERSION_v1}")
app.include_router(salary_router, prefix=f"/{API_VERSION_v1}", dependencies=[Depends(check_token)])

