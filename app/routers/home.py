from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.auth import require_login

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request):
    if request.session.get("logged_in"):
        return RedirectResponse(
            url="/welcome",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "Fake Job Detection System"
        }
    )


@router.get("/welcome")
def welcome(request: Request):
    login_redirect = require_login(request)

    if login_redirect:
        return login_redirect

    return templates.TemplateResponse(
        request=request,
        name="welcome.html",
        context={
            "title": "Welcome",
            "user_name": request.session.get("user_name")
        }
    )


@router.get("/about")
def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "title": "About"
        }
    )


@router.get("/help")
def help_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="help.html",
        context={
            "title": "Help"
        }
    )
