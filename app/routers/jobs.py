from fastapi import APIRouter, Request, Depends, Form
from datetime import datetime
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import require_login

from app.schemas.job import JobCreate

from app.services.job_service import (
    create_job,
    get_all_jobs,
    get_job_by_id,
    update_job,
    delete_job_by_id
)

router = APIRouter(prefix="/jobs")

templates = Jinja2Templates(
    directory="app/templates"
)

# =====================================================
# Add Job Page
# =====================================================

@router.get("/add")
def add_job_page(request: Request):

    login_redirect = require_login(request)

    if login_redirect:
        return login_redirect

    return templates.TemplateResponse(
        request=request,
        name="add_job.html",
        context={
            "title": "Add Job"
        }
    )


# =====================================================
# Save Job
# =====================================================

@router.post("/add")
def add_job(
    request: Request,

    title: str = Form(...),
    company: str = Form(...),
    location: str = Form(""),
    department: str = Form(""),
    salary_range: str = Form(""),
    company_profile: str = Form(""),
    description: str = Form(...),
    requirements: str = Form(""),
    benefits: str = Form(""),

    telecommuting: bool = Form(False),
    has_company_logo: bool = Form(False),
    has_questions: bool = Form(False),

    employment_type: str = Form(""),
    required_experience: str = Form(""),
    required_education: str = Form(""),
    industry: str = Form(""),
    function: str = Form(""),

    application_deadline: str = Form(""),
    job_link: str = Form(""),

    db: Session = Depends(get_db)
):

    login_redirect = require_login(request)

    if login_redirect:
        return login_redirect

    job = JobCreate(

        title=title,
        company=company,
        location=location,
        department=department,
        salary_range=salary_range,
        company_profile=company_profile,
        description=description,
        requirements=requirements,
        benefits=benefits,

        telecommuting=telecommuting,
        has_company_logo=has_company_logo,
        has_questions=has_questions,

        employment_type=employment_type,
        required_experience=required_experience,
        required_education=required_education,
        industry=industry,
        function=function,

        application_deadline=(
            datetime.fromisoformat(application_deadline)
            if application_deadline
            else None
),

job_link=job_link if job_link else None
    )

    create_job(
        db=db,
        job=job,
        user_id=request.session["user_id"]
    )

    return RedirectResponse(
        url="/jobs?success=Job+added+successfully",
        status_code=303
    )


# =====================================================
# My Jobs
# =====================================================

@router.get("")
def my_jobs(
    request: Request,
    db: Session = Depends(get_db)
):

    login_redirect = require_login(request)

    if login_redirect:
        return login_redirect

    jobs = get_all_jobs(
        db,
        request.session["user_id"]
    )

    return templates.TemplateResponse(
        request=request,
        name="jobs.html",
        context={
            "title": "My Jobs",
            "jobs": jobs
        }
    )


# =====================================================
# Job Details
# =====================================================

@router.get("/{job_id}")
def view_job(
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

    return templates.TemplateResponse(
        request=request,
        name="job_details.html",
        context={
            "title": "Job Details",
            "job": job
        }
    )

# =====================================================
# Edit Job Page
# =====================================================

@router.get("/{job_id}/edit")
def edit_job_page(
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
                "message": "The requested job does not exist or you do not have permission to edit it."
            },
            status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="edit_job.html",
        context={
            "title": "Edit Job",
            "job": job
        }
    )


# =====================================================
# Update Job
# =====================================================

@router.post("/{job_id}/edit")
def edit_job(
    job_id: int,
    request: Request,

    title: str = Form(...),
    company: str = Form(...),
    location: str = Form(""),
    department: str = Form(""),
    salary_range: str = Form(""),
    company_profile: str = Form(""),
    description: str = Form(...),
    requirements: str = Form(""),
    benefits: str = Form(""),

    telecommuting: bool = Form(False),
    has_company_logo: bool = Form(False),
    has_questions: bool = Form(False),

    employment_type: str = Form(""),
    required_experience: str = Form(""),
    required_education: str = Form(""),
    industry: str = Form(""),
    function: str = Form(""),
    application_deadline: str = Form(""),
    job_link: str = Form(""),

    db: Session = Depends(get_db)
):

    login_redirect = require_login(request)

    if login_redirect:
        return login_redirect

    db_job = get_job_by_id(
        db,
        job_id,
        request.session["user_id"]
    )

    if db_job is None:

        return templates.TemplateResponse(
            request=request,
            name="errors/404.html",
            context={
                "title": "Job Not Found",
                "message": "Unable to update the selected job."
            },
            status_code=404
        )

    updated_job = JobCreate(
        title=title,
        company=company,
        location=location,
        department=department,
        salary_range=salary_range,
        company_profile=company_profile,
        description=description,
        requirements=requirements,
        benefits=benefits,
        telecommuting=telecommuting,
        has_company_logo=has_company_logo,
        has_questions=has_questions,
        employment_type=employment_type,
        required_experience=required_experience,
        required_education=required_education,
        industry=industry,
        function=function,

        application_deadline=(
            datetime.fromisoformat(application_deadline)
            if application_deadline
            else None
        ),

        job_link=job_link if job_link else None
    )

    update_job(
        db=db,
        db_job=db_job,
        job=updated_job
    )

    return RedirectResponse(
        url="/jobs?success=Job+updated+successfully",
        status_code=303
    )


# =====================================================
# Delete Job
# =====================================================

@router.get("/{job_id}/delete")
def delete_job(
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
                "message": "The requested job does not exist or has already been deleted."
            },
            status_code=404
        )

    delete_job_by_id(
        db,
        job_id,
        request.session["user_id"]
    )

    return RedirectResponse(
        url="/jobs?success=Job+deleted+successfully",
        status_code=303
    )