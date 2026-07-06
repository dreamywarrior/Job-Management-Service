from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import require_login

from app.services.job_service import get_job_by_id
from app.services.prediction_service import (
    predict_job,
    get_prediction_history,
    get_prediction_by_id
)

router = APIRouter(prefix="/prediction")

templates = Jinja2Templates(
    directory="app/templates"
)

# =====================================================
# Prediction History
# =====================================================

@router.get("/history")
def prediction_history(
    request: Request,
    db: Session = Depends(get_db)
):

    login_redirect = require_login(request)

    if login_redirect:
        return login_redirect

    history = get_prediction_history(
        db,
        request.session["user_id"]
    )

    return templates.TemplateResponse(
        request=request,
        name="prediction_history.html",
        context={
            "title": "Prediction History",
            "history": history
        }
    )

# =====================================================
# Prediction Details
# =====================================================

@router.get("/details/{prediction_id}")
def prediction_details(
    prediction_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    login_redirect = require_login(request)

    if login_redirect:
        return login_redirect

    prediction = get_prediction_by_id(
        db,
        prediction_id,
        request.session["user_id"]
    )

    if prediction is None:

        return templates.TemplateResponse(
            request=request,
            name="errors/404.html",
            context={
                "title": "Prediction Not Found",
                "message": "The requested prediction could not be found."
            },
            status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="prediction_details.html",
        context={
            "title": "Prediction Details",
            "prediction": prediction
        }
    )

# =====================================================
# Predict Job
# =====================================================

@router.get("/{job_id}")
def verify_job(
    job_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    login_redirect = require_login(request)

    if login_redirect:
        return login_redirect

    job = get_job_by_id(
        db,
        job_id,
        request.session["user_id"]
    )

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
                "message": "Unable to generate prediction."
            },
            status_code=500
        )

    return templates.TemplateResponse(
        request=request,
        name="prediction_result.html",
        context={
            "title": "Prediction Result",
            "job": job,
            "prediction": result
        }
    )
