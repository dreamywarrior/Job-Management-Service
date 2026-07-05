import random

from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.prediction_result import PredictionResult


def predict_job(
    db: Session,
    job: Job
):

    prediction = random.choice(
        [
            "Legitimate",
            "Fake"
        ]
    )

    confidence = round(
        random.uniform(85, 99),
        2
    )

    existing_prediction = (
        db.query(PredictionResult)
        .filter(PredictionResult.job_id == job.id)
        .first()
    )

    if existing_prediction:

        existing_prediction.prediction = prediction
        existing_prediction.confidence = confidence

        db.commit()
        db.refresh(existing_prediction)

        return existing_prediction

    result = PredictionResult(
        job_id=job.id,
        prediction=prediction,
        confidence=confidence
    )

    db.add(result)

    db.commit()

    db.refresh(result)

    return result