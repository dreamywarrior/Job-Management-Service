from sqlalchemy.orm import Session, joinedload

from app.models.job import Job
from app.models.prediction_result import PredictionResult


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

    # --------------------------------------------------
    # Return
    # --------------------------------------------------

    return {
        "total_jobs": total_jobs,
        "total_predictions": total_predictions,
        "fake_jobs": fake_jobs,
        "legitimate_jobs": legitimate_jobs,
        "pending_jobs": pending_jobs,
        "recent_jobs": recent_jobs,
    }