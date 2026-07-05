from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.core.database import get_db

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

    if not request.session.get("logged_in"):

        return RedirectResponse(
            url="/auth/login",
            status_code=303
        )

    job = get_job_by_id(
        db,
        job_id,
        request.session["user_id"]
    )

    if job is None:

        return RedirectResponse(
            url="/jobs",
            status_code=303
        )

    result = predict_job(
        db,
        job
    )

    return templates.TemplateResponse(
        request=request,
        name="prediction_result.html",
        context={
            "title": "Prediction",

            "job": job,

            "prediction": result
        }
    )