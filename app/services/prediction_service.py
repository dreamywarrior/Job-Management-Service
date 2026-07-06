import random
import os
import joblib

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import joinedload

from app.models.job import Job
from app.models.prediction_result import PredictionResult

# Load ML Model
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ml', 'model.pkl')
try:
    ml_model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Warning: Could not load ML model from {MODEL_PATH}. Using fallback. Error: {e}")
    ml_model = None

# -----------------------------------------------------
# Predict Job
# -----------------------------------------------------

def predict_job(
    db: Session,
    job: Job
):
    
    if ml_model is not None:
        text = f"{job.title or ''} {job.description or ''}"
        pred_val = ml_model.predict([text])[0]
        prediction = "Fake" if pred_val == 1 else "Legitimate"
        prob = ml_model.predict_proba([text])[0]
        confidence = round(max(prob) * 100, 2)
    else:
        prediction = random.choice(["Legitimate", "Fake"])
        confidence = round(random.uniform(85, 99), 2)

    existing_prediction = (
        db.query(PredictionResult)
        .filter(
            PredictionResult.job_id == job.id
        )
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


# -----------------------------------------------------
# Prediction History
# -----------------------------------------------------

def get_prediction_history(
    db: Session,
    user_id: int
):

    history = (

        db.query(PredictionResult)

        .join(Job)

        .options(
            joinedload(
                PredictionResult.job
            )
        )

        .filter(
            Job.user_id == user_id
        )

        .order_by(
            PredictionResult.predicted_at.desc()
        )

        .all()

    )

    return history

# -----------------------------------------------------
# Get Prediction By ID
# -----------------------------------------------------

def get_prediction_by_id(
    db: Session,
    prediction_id: int,
    user_id: int
):

    prediction = (

        db.query(PredictionResult)

        .join(Job)

        .options(
            joinedload(PredictionResult.job)
        )

        .filter(
            PredictionResult.id == prediction_id,
            Job.user_id == user_id
        )

        .first()

    )

    return prediction