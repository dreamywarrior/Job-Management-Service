from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta

from app.models import job
from app.models.job import Job
from app.schemas.job import JobCreate

# ---------------------------------------------------
# Deadline Status
# ---------------------------------------------------

def get_deadline_status(deadline):

    if deadline is None:
        return {
            "label": "Not Set",
            "badge": "secondary"
        }

    now = datetime.now()

    if deadline < now:
        return {
            "label": "Expired",
            "badge": "danger"
        }

    remaining = deadline - now

    if remaining <= timedelta(hours=1):
        return {
            "label": "Less than 1 hour left",
            "badge": "danger"
        }

    if remaining <= timedelta(hours=5):
        hours = int(remaining.total_seconds() // 3600)

        return {
            "label": f"{hours} hour(s) left",
            "badge": "warning"
        }

    if remaining <= timedelta(days=1):
        hours = int(remaining.total_seconds() // 3600)

        return {
            "label": f"{hours} hour(s) left",
            "badge": "warning"
        }

    days = remaining.days

    return {
        "label": f"{days} day(s) left",
        "badge": "success"
    }

# ---------------------------------------------------
# Create Job
# ---------------------------------------------------

def create_job(
    db: Session,
    job: JobCreate,
    user_id: int
):

    db_job = Job(

        user_id=user_id,

        title=job.title,
        company=job.company,
        location=job.location,
        department=job.department,
        salary_range=job.salary_range,
        company_profile=job.company_profile,

        description=job.description,
        requirements=job.requirements,
        benefits=job.benefits,

        telecommuting=job.telecommuting,
        has_company_logo=job.has_company_logo,
        has_questions=job.has_questions,

        employment_type=job.employment_type,
        required_experience=job.required_experience,
        required_education=job.required_education,

        industry=job.industry,
        function=job.function,

        application_deadline=job.application_deadline,
        job_link=str(job.job_link) if job.job_link else None
    )

    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job


# ---------------------------------------------------
# Get All Jobs
# ---------------------------------------------------

def get_all_jobs(db, user_id):

    jobs = (
        db.query(Job)
        .options(
            joinedload(Job.prediction_result)
        )
        .filter(Job.user_id == user_id)
        .order_by(Job.created_at.desc())
        .all()
    )

    for job in jobs:

        job.deadline_status = get_deadline_status(
            job.application_deadline
        )

    return jobs


# ---------------------------------------------------
# Get Single Job
# ---------------------------------------------------

def get_job_by_id(
    db: Session,
    job_id: int,
    user_id: int
):

    return (
        db.query(Job)
        .filter(
            Job.id == job_id,
            Job.user_id == user_id
        )
        .first()
    )


# ---------------------------------------------------
# Update Job
# ---------------------------------------------------

def update_job(
    db: Session,
    db_job: Job,
    job: JobCreate
):

    db_job.title = job.title
    db_job.company = job.company
    db_job.location = job.location
    db_job.department = job.department
    db_job.salary_range = job.salary_range
    db_job.company_profile = job.company_profile

    db_job.description = job.description
    db_job.requirements = job.requirements
    db_job.benefits = job.benefits

    db_job.telecommuting = job.telecommuting
    db_job.has_company_logo = job.has_company_logo
    db_job.has_questions = job.has_questions

    db_job.employment_type = job.employment_type
    db_job.required_experience = job.required_experience
    db_job.required_education = job.required_education

    db_job.industry = job.industry
    db_job.function = job.function

    db_job.application_deadline = job.application_deadline
    db_job.job_link = (
        str(job.job_link)
        if job.job_link
        else None
    )

    # Editing a job changes the source text, so any old prediction is stale.
    from app.services.prediction_service import delete_prediction

    delete_prediction(
        db,
        db_job.id
    )

    db.commit()
    db.refresh(db_job)

    return db_job


# ---------------------------------------------------
# Delete Job
# ---------------------------------------------------

def delete_job_by_id(
    db: Session,
    job_id: int,
    user_id: int
):

    job = get_job_by_id(
        db,
        job_id,
        user_id
    )

    if job:
        db.delete(job)
        db.commit()


# ---------------------------------------------------
# Dashboard Statistics
# ---------------------------------------------------

def get_job_count(
    db: Session,
    user_id: int
):

    return (
        db.query(Job)
        .filter(Job.user_id == user_id)
        .count()
    )


# ---------------------------------------------------
# Recent Jobs
# ---------------------------------------------------

def get_recent_jobs(
    db: Session,
    user_id: int,
    limit: int = 5
):

    return (
        db.query(Job)
        .filter(Job.user_id == user_id)
        .order_by(Job.created_at.desc())
        .limit(limit)
        .all()
    )
