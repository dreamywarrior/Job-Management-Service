from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.routers.home import router as home_router
from app.routers.auth import router as auth_router
from app.routers.dashboard import router as dashboard_router
from app.routers.jobs import router as jobs_router
from app import models
from app.routers.prediction import router as prediction_router

app = FastAPI(
    title="Job Management Service",
    description="Fake Job Posting Detection System",
    version="1.0.0"
)

app.add_middleware(
    SessionMiddleware,
    secret_key="change_this_to_a_long_random_secret_key"
)

# Static Files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(home_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(jobs_router)
app.include_router(prediction_router)