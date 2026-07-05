from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.prediction_result import PredictionResult


def get_dashboard_stats(db: Session, user_id: int):

    total_jobs = (
        db.query(Job)
        .filter(Job.user_id == user_id)
        .count()
    )

    total_predictions = (
        db.query(PredictionResult)
        .join(Job)
        .filter(Job.user_id == user_id)
        .count()
    )

    fake_jobs = (
        db.query(PredictionResult)
        .join(Job)
        .filter(
            Job.user_id == user_id,
            PredictionResult.prediction == "Fake"
        )
        .count()
    )

    recent_jobs = (
        db.query(Job)
        .filter(Job.user_id == user_id)
        .order_by(Job.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "total_jobs": total_jobs,
        "total_predictions": total_predictions,
        "fake_jobs": fake_jobs,
        "recent_jobs": recent_jobs
    }