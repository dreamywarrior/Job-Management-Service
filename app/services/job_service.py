from sqlalchemy.orm import Session, joinedload

from app.models.job import Job
from app.schemas.job import JobCreate


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
        function=job.function
    )

    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job


# ---------------------------------------------------
# Get All Jobs
# ---------------------------------------------------

def get_all_jobs(db, user_id):

    return (
        db.query(Job)
        .options(
            joinedload(Job.prediction_result)
        )
        .filter(Job.user_id == user_id)
        .order_by(Job.created_at.desc())
        .all()
    )


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