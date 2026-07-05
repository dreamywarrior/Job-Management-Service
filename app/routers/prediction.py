from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import require_login

from app.services.job_service import get_job_by_id
from app.services.prediction_service import predict_job

router = APIRouter(prefix="/prediction")

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/{job_id}")
def verify_job(
    job_id: int,
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
    # Fetch Job
    # ---------------------------------------

    job = get_job_by_id(
        db,
        job_id,
        request.session["user_id"]
    )

    # ---------------------------------------
    # Job Not Found
    # ---------------------------------------

    if job is None:

        return templates.TemplateResponse(
            request=request,
            name="errors/404.html",
            context={
                "title": "Job Not Found",
                "message": "The requested job could not be found."
            },
            status_code=404
        )

    # ---------------------------------------
    # Run Prediction
    # ---------------------------------------

    try:

        result = predict_job(
            db,
            job
        )

    except Exception:

        return templates.TemplateResponse(
            request=request,
            name="errors/500.html",
            context={
                "title": "Prediction Error",
                "message": (
                    "Unable to contact the prediction service. "
                    "Please try again later."
                )
            },
            status_code=500
        )

    # ---------------------------------------
    # Render Result
    # ---------------------------------------

    return templates.TemplateResponse(
        request=request,
        name="prediction_result.html",
        context={
            "title": "Prediction Result",
            "job": job,
            "prediction": result
        }
    )