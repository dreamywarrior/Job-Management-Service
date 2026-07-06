import re

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate
from app.services.auth_service import (
    create_user,
    authenticate_user,
    get_user_by_email,
    get_user_by_id,
    update_profile,
    change_password
)

router = APIRouter(prefix="/auth")

templates = Jinja2Templates(directory="app/templates")


# =====================================================
# Password Policy
# =====================================================

PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])"
    r"(?=.*[A-Z])"
    r"(?=.*\d)"
    r"(?=.*[@$!%*?&^#()_+\-=\[\]{};':\"\\|,.<>/~`]).{8,}$"
)


# =====================================================
# Register Page
# =====================================================

@router.get("/register")
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "title": "Register"
        }
    )


# =====================================================
# Register User
# =====================================================

@router.post("/register")
def register_user(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    # ---------------------------------------
    # Check duplicate email FIRST
    # ---------------------------------------

    existing_user = get_user_by_email(db, email)

    if existing_user:

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "title": "Register",
                "error": (
                    "An account with this email address already exists. "
                    "Please log in or use a different email."
                ),
                "full_name": full_name,
                "email": email
            }
        )

    # ---------------------------------------
    # Validate Password
    # ---------------------------------------

    if not PASSWORD_REGEX.match(password):

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "title": "Register",
                "error": (
                    "Password must contain at least 8 characters, "
                    "one uppercase letter, one lowercase letter, "
                    "one number and one special character."
                ),
                "full_name": full_name,
                "email": email
            }
        )

    # ---------------------------------------
    # Create User
    # ---------------------------------------

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
                "error": str(e),
                "full_name": full_name,
                "email": email
            }
        )

    return RedirectResponse(
        url="/auth/login?success=Registration successful. Please login.",
        status_code=303
    )


# =====================================================
# Login Page
# =====================================================

@router.get("/login")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "title": "Login"
        }
    )


# =====================================================
# Login User
# =====================================================

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
                "error": "Invalid email or password.",
                "email": email
            }
        )

    # ---------------------------------------
    # Create Session
    # ---------------------------------------

    request.session["user_id"] = user.id
    request.session["user_name"] = user.full_name
    request.session["logged_in"] = True

    return RedirectResponse(
        url="/dashboard?success=Login successful.",
        status_code=303
    )

# =====================================================
# Profile
# =====================================================

@router.get("/profile", response_class=HTMLResponse)
def profile(
    request: Request,
    db: Session = Depends(get_db)
):

    # ---------------------------------------
    # Check Login
    # ---------------------------------------

    if not request.session.get("logged_in"):

        return RedirectResponse(
            url="/auth/login",
            status_code=303
        )

    user = get_user_by_id(
        db,
        request.session.get("user_id")
    )

    # ---------------------------------------
    # User no longer exists
    # (database recreated / stale session)
    # ---------------------------------------

    if user is None:

        request.session.clear()

        return RedirectResponse(
            url="/auth/login?error=Your session has expired. Please login again.",
            status_code=303
        )

    # Keep session name synchronized
    request.session["user_name"] = user.full_name

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "title": "My Profile",
            "user": user
        }
    )

# =====================================================
# Edit Profile
# =====================================================

@router.get("/profile/edit")
def edit_profile_page(
    request: Request,
    db: Session = Depends(get_db)
):

    if not request.session.get("logged_in"):

        return RedirectResponse(
            url="/auth/login",
            status_code=303
        )

    user = get_user_by_id(
        db,
        request.session["user_id"]
    )

    if user is None:

        request.session.clear()

        return RedirectResponse(
            "/auth/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="edit_profile.html",
        context={
            "title": "Edit Profile",
            "user": user
        }
    )

@router.post("/profile/edit")
def edit_profile(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):

    if not request.session.get("logged_in"):

        return RedirectResponse(
            "/auth/login",
            status_code=303
        )

    try:

        user = update_profile(
            db,
            request.session["user_id"],
            full_name,
            email
        )

        request.session["user_name"] = user.full_name

    except ValueError as e:

        user = get_user_by_id(
            db,
            request.session["user_id"]
        )

        return templates.TemplateResponse(
            request=request,
            name="edit_profile.html",
            context={
                "title": "Edit Profile",
                "user": user,
                "error": str(e)
            }
        )

    return RedirectResponse(
        "/auth/profile",
        status_code=303
    )

# =====================================================
# Change Password
# =====================================================

@router.get("/change-password")
def change_password_page(
    request: Request
):

    if not request.session.get("logged_in"):

        return RedirectResponse(
            "/auth/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="change_password.html",
        context={
            "title": "Change Password"
        }
    )

@router.post("/change-password")
def update_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):

    if not request.session.get("logged_in"):

        return RedirectResponse(
            "/auth/login",
            status_code=303
        )

    if new_password != confirm_password:

        return templates.TemplateResponse(
            request=request,
            name="change_password.html",
            context={
                "title": "Change Password",
                "error": "Passwords do not match."
            }
        )

    if not PASSWORD_REGEX.match(new_password):

        return templates.TemplateResponse(
            request=request,
            name="change_password.html",
            context={
                "title": "Change Password",
                "error": (
                    "Password must contain at least 8 characters, "
                    "one uppercase letter, one lowercase letter, "
                    "one number and one special character."
                )
            }
        )

    try:

        change_password(
            db,
            request.session["user_id"],
            current_password,
            new_password
        )

    except ValueError as e:

        return templates.TemplateResponse(
            request=request,
            name="change_password.html",
            context={
                "title": "Change Password",
                "error": str(e)
            }
        )

    return RedirectResponse(
        "/auth/profile",
        status_code=303
    )

# =====================================================
# Logout
# =====================================================

@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/?success=Logged out successfully.",
        status_code=303
    )