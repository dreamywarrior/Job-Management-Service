from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

from app.core.database import Base, engine

from app.routers import (
    home,
    auth,
    dashboard,
    jobs,
    prediction
)

# -------------------------------------------------
# Create Database Tables
# -------------------------------------------------

Base.metadata.create_all(bind=engine)

# -------------------------------------------------
# FastAPI App
# -------------------------------------------------

app = FastAPI(
    title="Fake Job Detection System"
)

# -------------------------------------------------
# Session Middleware
# -------------------------------------------------

app.add_middleware(
    SessionMiddleware,
    secret_key="change_this_to_a_secure_random_key"
)

# -------------------------------------------------
# Static Files
# -------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# -------------------------------------------------
# Templates
# -------------------------------------------------

templates = Jinja2Templates(
    directory="app/templates"
)

# -------------------------------------------------
# Routers
# -------------------------------------------------

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(jobs.router)
app.include_router(prediction.router)

# =================================================
# Custom Error Pages
# =================================================

@app.exception_handler(404)
async def custom_404_handler(
    request: Request,
    exc
):

    return templates.TemplateResponse(
        request=request,
        name="errors/404.html",
        context={
            "title": "404",
            "message": "The page you requested could not be found."
        },
        status_code=404
    )


@app.exception_handler(500)
async def custom_500_handler(
    request: Request,
    exc
):

    return templates.TemplateResponse(
        request=request,
        name="errors/500.html",
        context={
            "title": "500",
            "message": "Something went wrong while processing your request."
        },
        status_code=500
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception
):

    print(exc)

    return templates.TemplateResponse(
        request=request,
        name="errors/500.html",
        context={
            "title": "Server Error",
            "message": str(exc)
        },
        status_code=500
    )