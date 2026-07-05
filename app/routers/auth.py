from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate
from app.services.auth_service import create_user, authenticate_user

router = APIRouter(prefix="/auth")

templates = Jinja2Templates(directory="app/templates")


# -----------------------------
# Register Page
# -----------------------------
@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "title": "Register"
        }
    )


# -----------------------------
# Register User
# -----------------------------
@router.post("/register")
def register_user(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = UserCreate(
        full_name=full_name,
        email=email,
        password=password
    )

    try:
        create_user(db, user)

    except ValueError as e:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "title": "Register",
                "error": str(e)
            }
        )

    return RedirectResponse(
        url="/auth/login",
        status_code=303
    )


# -----------------------------
# Login Page
# -----------------------------
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "title": "Login"
        }
    )


# -----------------------------
# Login User
# -----------------------------
@router.post("/login")
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        email,
        password
    )

    if user is None:

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "title": "Login",
                "error": "Invalid email or password"
            }
        )

    # Create Session
    request.session["user_id"] = user.id
    request.session["user_name"] = user.full_name
    request.session["logged_in"] = True

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )


# -----------------------------
# Logout
# -----------------------------
@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )