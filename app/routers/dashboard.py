from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard_service import get_dashboard_stats

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    if not request.session.get("logged_in"):
        return RedirectResponse(
            url="/auth/login",
            status_code=303
        )

    stats = get_dashboard_stats(
        db,
        request.session["user_id"]
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "title": "Dashboard",
            **stats
        }
    )