from fastapi import FastAPI
from app.api.routes import health_check, work_route

app = FastAPI()

app.include_router(health_check.router)
app.include_router(work_route.router)