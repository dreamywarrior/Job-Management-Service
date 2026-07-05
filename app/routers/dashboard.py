from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.auth import require_login
from app.core.database import get_db
from app.services.dashboard_service import get_dashboard_stats

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    # ---------------------------------------
    # Login Required
    # ---------------------------------------

    login_redirect = require_login(request)

    if login_redirect:
        return login_redirect

    # ---------------------------------------
    # Dashboard Statistics
    # ---------------------------------------

    stats = get_dashboard_stats(
        db,
        request.session["user_id"]
    )

    # ---------------------------------------
    # Render Dashboard
    # ---------------------------------------

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "title": "Dashboard",
            **stats
        }
    )