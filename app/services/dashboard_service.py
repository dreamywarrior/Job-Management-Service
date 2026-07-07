from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta

from app.models.job import Job
from app.models.prediction_result import PredictionResult
from app.services.job_service import get_deadline_status
from app.services.prediction_service import (
    get_prediction_statistics,
    get_dashboard_insights,
    get_recent_predictions,
    get_top_suspicious_jobs,
    get_confidence_distribution,
    get_risk_distribution,
    get_company_distribution,
    get_location_distribution,
    get_employment_distribution,
)

now = datetime.now()

def get_dashboard_stats(db: Session, user_id: int):

    # --------------------------------------------------
    # Total Jobs
    # --------------------------------------------------

    total_jobs = (
        db.query(Job)
        .filter(Job.user_id == user_id)
        .count()
    )

    # --------------------------------------------------
    # Total Predictions
    # --------------------------------------------------

    total_predictions = (
        db.query(PredictionResult)
        .join(Job)
        .filter(Job.user_id == user_id)
        .count()
    )

    # --------------------------------------------------
    # Fake Jobs
    # --------------------------------------------------

    fake_jobs = (
        db.query(PredictionResult)
        .join(Job)
        .filter(
            Job.user_id == user_id,
            PredictionResult.prediction == "Fake"
        )
        .count()
    )

    # --------------------------------------------------
    # Legitimate Jobs
    # --------------------------------------------------

    legitimate_jobs = (
        db.query(PredictionResult)
        .join(Job)
        .filter(
            Job.user_id == user_id,
            PredictionResult.prediction == "Legitimate"
        )
        .count()
    )

    # --------------------------------------------------
    # Pending Jobs
    # --------------------------------------------------

    pending_jobs = max(
        total_jobs - total_predictions,
        0
    )

    prediction_stats = get_prediction_statistics(
        db,
        user_id
    )

    # --------------------------------------------------
    # Confidence Statistics
    # --------------------------------------------------

    predictions = (
        db.query(PredictionResult)
        .join(Job)
        .filter(Job.user_id == user_id)
        .all()
    )

    if predictions:

        average_confidence = prediction_stats["average_confidence"]

        highest_confidence = prediction_stats["highest_confidence"]

    else:

        average_confidence = 0

        highest_confidence = 0

    high_risk_jobs = prediction_stats["high_risk_jobs"]

    # --------------------------------------------------
    # Recent Jobs
    # --------------------------------------------------

    recent_jobs = (
        db.query(Job)
        .options(joinedload(Job.prediction_result))
        .filter(Job.user_id == user_id)
        .order_by(Job.created_at.desc())
        .limit(5)
        .all()
    )

    for job in recent_jobs:
        job.deadline_status = get_deadline_status(
            job.application_deadline
        )

    # --------------------------------------------------
    # Upcoming Deadlines (Next 24 Hours)
    # --------------------------------------------------

    upcoming_deadlines = (
        db.query(Job)
        .filter(
            Job.user_id == user_id,
            Job.application_deadline != None,
            Job.application_deadline >= now,
            Job.application_deadline <= now + timedelta(hours=24)
        )
        .order_by(Job.application_deadline.asc())
        .limit(5)
        .all()
    )

    # --------------------------------------------------
    # Overdue Jobs
    # --------------------------------------------------

    overdue_jobs = (
        db.query(Job)
        .filter(
            Job.user_id == user_id,
            Job.application_deadline != None,
            Job.application_deadline < now
        )
        .count()
    )

    # --------------------------------------------------
    # Jobs Without Deadline
    # --------------------------------------------------

    jobs_without_deadline = (
        db.query(Job)
        .filter(
            Job.user_id == user_id,
            Job.application_deadline == None
        )
        .count()
    )

    remote_jobs = (
        db.query(Job)
        .filter(
            Job.user_id == user_id,
            Job.telecommuting == 1
        )
        .count()
    )

    jobs_with_logo = (
        db.query(Job)
        .filter(
            Job.user_id == user_id,
            Job.has_company_logo == 1
        )
        .count()
    )

    jobs_with_questions = (
        db.query(Job)
        .filter(
            Job.user_id == user_id,
            Job.has_questions == 1
        )
        .count()
    )


    alerts = get_deadline_alerts(
        db,
        user_id
    )

    # --------------------------------------------------
    # Return
    # --------------------------------------------------

    dashboard_insights = get_dashboard_insights(
        db,
        user_id
    )

    recent_predictions = get_recent_predictions(
        db,
        user_id
    )

    suspicious_jobs = get_top_suspicious_jobs(
        db,
        user_id
    )

    confidence_distribution = get_confidence_distribution(
        db,
        user_id
    )

    risk_distribution = get_risk_distribution(
        db,
        user_id
    )

    company_distribution = get_company_distribution(
        db,
        user_id
    )

    location_distribution = get_location_distribution(
        db,
        user_id
    )

    employment_distribution = get_employment_distribution(
        db,
        user_id
    )

    return {

        "total_jobs": total_jobs,

        "total_predictions": total_predictions,

        "fake_jobs": fake_jobs,

        "legitimate_jobs": legitimate_jobs,

        "pending_jobs": pending_jobs,

        "average_confidence": average_confidence,

        "highest_confidence": highest_confidence,

        "high_risk_jobs": high_risk_jobs,

        "recent_jobs": recent_jobs,

        "upcoming_deadlines": upcoming_deadlines,

        "overdue_jobs": overdue_jobs,

        "jobs_without_deadline": jobs_without_deadline,

        "deadline_alerts": alerts,

        "prediction_statistics": prediction_stats,

        "dashboard_insights": dashboard_insights,

        "recent_predictions": recent_predictions,

        "top_suspicious_jobs": suspicious_jobs,

        "confidence_distribution": to_chart_data(confidence_distribution),

        "risk_distribution": to_chart_data(risk_distribution),

        "company_distribution": to_chart_data(company_distribution),

        "location_distribution": to_chart_data(location_distribution),

        "employment_distribution": to_chart_data(employment_distribution),

        "remote_jobs": remote_jobs,

        "jobs_with_logo": jobs_with_logo,

        "jobs_with_questions": jobs_with_questions,

        "monthly_jobs": to_chart_data(get_monthly_jobs(db, user_id)),

        "industry_distribution": to_chart_data(get_industry_distribution(db, user_id)),

    }

# ---------------------------------------------------
# Deadline Alerts
# ---------------------------------------------------

def get_deadline_alerts(
    db: Session,
    user_id: int
):

    jobs = (
        db.query(Job)
        .filter(
            Job.user_id == user_id,
            Job.application_deadline != None
        )
        .order_by(Job.application_deadline.asc())
        .all()
    )

    alerts = []

    now = datetime.now()

    for job in jobs:

        remaining = job.application_deadline - now

        if remaining.total_seconds() < 0:

            continue

        hours = remaining.total_seconds() / 3600

        if hours <= 1:

            alerts.append({

                "type": "danger",

                "title": "Final Reminder",

                "message":
                    f"{job.title} at {job.company} closes within 1 hour.",

                "job": job

            })

        elif hours <= 5:

            alerts.append({

                "type": "warning",

                "title": "Upcoming Deadline",

                "message":
                    f"{job.title} at {job.company} closes within 5 hours.",

                "job": job

            })

        elif hours <= 24:

            alerts.append({

                "type": "info",

                "title": "Application Deadline Tomorrow",

                "message":
                    f"{job.title} at {job.company} closes within 24 hours.",

                "job": job

            })

    return alerts

# ---------------------------------------------------
# Monthly Jobs
# ---------------------------------------------------

def get_monthly_jobs(db: Session, user_id: int):

    jobs = (
        db.query(Job)
        .filter(Job.user_id == user_id)
        .order_by(Job.created_at.asc())
        .all()
    )

    months = {}

    for job in jobs:

        month = job.created_at.strftime("%b %Y")

        months[month] = months.get(month, 0) + 1

    return months

# ---------------------------------------------------
# Industry Distribution
# ---------------------------------------------------

def get_industry_distribution(
    db: Session,
    user_id: int
):

    jobs = (
        db.query(Job)
        .filter(Job.user_id == user_id)
        .all()
    )

    result = {}

    for job in jobs:

        industry = job.industry or "Unknown"

        result[industry] = result.get(industry, 0) + 1

    return result

def to_chart_data(data: dict):

    return {
        "labels": list(data.keys()),
        "values": list(data.values())
    }
