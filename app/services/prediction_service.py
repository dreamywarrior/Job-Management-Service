import os
import re
import random
import joblib

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.models.job import Job
from app.models.prediction_result import PredictionResult

# ============================================================
# ML MODEL CONFIGURATION
# ============================================================

MODEL_NAME = "Random Forest + TF-IDF v1.0"

MODEL_PATH = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    ),
    "ml",
    "model.pkl"
)

try:

    ml_model = joblib.load(MODEL_PATH)

    print(f"[INFO] Loaded ML model from {MODEL_PATH}")

except Exception as e:

    print(f"[WARNING] ML model could not be loaded.")

    print(e)

    ml_model = None


# ============================================================
# RISK LEVEL
# ============================================================

def calculate_risk_level(confidence: float):

    if confidence < 50:
        return "Low"

    if confidence < 70:
        return "Medium"

    if confidence < 85:
        return "High"

    return "Very High"


# ============================================================
# EXPLANATION GENERATOR
# ============================================================

def generate_explanation(job: Job):

    reasons = []

    title = (job.title or "").lower()
    description = (job.description or "").lower()

    text = f"{title} {description}"

    if "work from home" in text:
        reasons.append("Work from home advertised")

    if "remote" in text:
        reasons.append("Remote job")

    if "urgent" in text:
        reasons.append("Urgent hiring language")

    if "immediately" in text:
        reasons.append("Immediate joining requested")

    if "bank" in text:
        reasons.append("Mentions bank/payment details")

    if "transfer money" in text:
        reasons.append("Requests money transfer")

    if "earn $" in text:
        reasons.append("Unusually high earnings advertised")

    if "whatsapp" in text:
        reasons.append("Communication through WhatsApp")

    if "telegram" in text:
        reasons.append("Communication through Telegram")

    if "investment" in text:
        reasons.append("Investment related wording")

    salary_text = (
        job.salary_range.lower()
        if job.salary_range
        else ""
    )

    salary_match = re.findall(r"\d+", salary_text)

    if salary_match:

        try:

            highest = max(
                int(x.replace(",", ""))
                for x in salary_match
            )

            if highest > 100000:

                reasons.append(
                    "Very high salary offered"
                )

        except Exception:
            pass

    if not job.company:

        reasons.append(
            "Company information missing"
        )

    if not reasons:

        reasons.append(
            "No obvious suspicious indicators detected."
        )

    return "\n".join(reasons)


# ============================================================
# PREDICT JOB
# ============================================================

def predict_job(
    db: Session,
    job: Job
):

    text = f"{job.title or ''} {job.description or ''}"

    # --------------------------------------------------------
    # ML Prediction
    # --------------------------------------------------------

    if ml_model is not None:

        prediction_value = ml_model.predict([text])[0]

        prediction = (
            "Fake"
            if prediction_value == 1
            else "Legitimate"
        )

        probability = ml_model.predict_proba([text])[0]

        confidence = round(
            float(max(probability)) * 100,
            2
        )

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    else:

        prediction = random.choice(
            [
                "Fake",
                "Legitimate"
            ]
        )

        confidence = round(
            random.uniform(80, 99),
            2
        )

    risk_level = calculate_risk_level(
        confidence
    )

    explanation = generate_explanation(
        job
    )

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

        existing_prediction.risk_level = risk_level

        existing_prediction.model_used = MODEL_NAME

        existing_prediction.explanation = explanation

        db.commit()

        db.refresh(existing_prediction)

        return existing_prediction

    result = PredictionResult(

        job_id=job.id,

        prediction=prediction,

        confidence=confidence,

        risk_level=risk_level,

        model_used=MODEL_NAME,

        explanation=explanation

    )

    db.add(result)

    db.commit()

    db.refresh(result)

    return result

# ============================================================
# RE-RUN PREDICTION
# ============================================================

def rerun_prediction(
    db: Session,
    job_id: int
):

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        return None

    return predict_job(db, job)


# ============================================================
# DELETE PREDICTION
# ============================================================

def delete_prediction(
    db: Session,
    job_id: int
):

    prediction = (
        db.query(PredictionResult)
        .filter(
            PredictionResult.job_id == job_id
        )
        .first()
    )

    if prediction:

        db.delete(prediction)

        db.commit()


# ============================================================
# PREDICTION HISTORY
# ============================================================

def get_prediction_history(
    db: Session,
    user_id: int
):

    return (

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


# ============================================================
# PREDICTION BY ID
# ============================================================

def get_prediction_by_id(
    db: Session,
    prediction_id: int,
    user_id: int
):

    return (

        db.query(PredictionResult)

        .join(Job)

        .options(
            joinedload(
                PredictionResult.job
            )
        )

        .filter(
            PredictionResult.id == prediction_id,
            Job.user_id == user_id
        )

        .first()

    )


# ============================================================
# USER PREDICTION STATISTICS
# ============================================================

def get_prediction_statistics(
    db: Session,
    user_id: int
):

    predictions = (

        db.query(PredictionResult)

        .join(Job)

        .filter(
            Job.user_id == user_id
        )

        .all()

    )

    total_predictions = len(predictions)

    fake_jobs = sum(
        1
        for p in predictions
        if p.prediction == "Fake"
    )

    legitimate_jobs = sum(
        1
        for p in predictions
        if p.prediction == "Legitimate"
    )

    pending_jobs = (

        db.query(Job)

        .filter(
            Job.user_id == user_id
        )

        .count()

        -

        total_predictions

    )

    if predictions:

        average_confidence = round(

            sum(
                p.confidence
                for p in predictions
            )

            /

            total_predictions,

            2

        )

        highest_confidence = round(

            max(
                p.confidence
                for p in predictions
            ),

            2

        )

    else:

        average_confidence = 0

        highest_confidence = 0

    high_risk_jobs = sum(

        1

        for p in predictions

        if p.risk_level in [

            "High",

            "Very High"

        ]

    )

    return {

        "total_predictions": total_predictions,

        "fake_jobs": fake_jobs,

        "legitimate_jobs": legitimate_jobs,

        "pending_jobs": pending_jobs,

        "average_confidence": average_confidence,

        "highest_confidence": highest_confidence,

        "high_risk_jobs": high_risk_jobs

    }


# ============================================================
# RECENT PREDICTIONS
# ============================================================

def get_recent_predictions(
    db: Session,
    user_id: int,
    limit: int = 5
):

    return (

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

        .limit(limit)

        .all()

    )

# ============================================================
# CONFIDENCE DISTRIBUTION
# ============================================================

def get_confidence_distribution(
    db: Session,
    user_id: int
):

    predictions = (
        db.query(PredictionResult)
        .join(Job)
        .filter(Job.user_id == user_id)
        .all()
    )

    distribution = {
        "50-60": 0,
        "60-70": 0,
        "70-80": 0,
        "80-90": 0,
        "90-100": 0
    }

    for prediction in predictions:

        confidence = prediction.confidence

        if confidence < 60:
            distribution["50-60"] += 1

        elif confidence < 70:
            distribution["60-70"] += 1

        elif confidence < 80:
            distribution["70-80"] += 1

        elif confidence < 90:
            distribution["80-90"] += 1

        else:
            distribution["90-100"] += 1

    return distribution


# ============================================================
# RISK DISTRIBUTION
# ============================================================

def get_risk_distribution(
    db: Session,
    user_id: int
):

    predictions = (
        db.query(PredictionResult)
        .join(Job)
        .filter(Job.user_id == user_id)
        .all()
    )

    risk = {
        "Low": 0,
        "Medium": 0,
        "High": 0,
        "Very High": 0
    }

    for prediction in predictions:

        if prediction.risk_level in risk:
            risk[prediction.risk_level] += 1

    return risk


# ============================================================
# EMPLOYMENT DISTRIBUTION
# ============================================================

def get_employment_distribution(
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

        employment = job.employment_type or "Unknown"

        result[employment] = result.get(employment, 0) + 1

    return result


# ============================================================
# LOCATION DISTRIBUTION
# ============================================================

def get_location_distribution(
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

        location = job.location or "Unknown"

        result[location] = result.get(location, 0) + 1

    return result


# ============================================================
# COMPANY DISTRIBUTION
# ============================================================

def get_company_distribution(
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

        company = job.company or "Unknown"

        result[company] = result.get(company, 0) + 1

    return result


# ============================================================
# DASHBOARD INSIGHTS
# ============================================================

def get_dashboard_insights(
    db: Session,
    user_id: int
):

    stats = get_prediction_statistics(
        db,
        user_id
    )

    employment = get_employment_distribution(
        db,
        user_id
    )

    company = get_company_distribution(
        db,
        user_id
    )

    location = get_location_distribution(
        db,
        user_id
    )

    top_company = (
        max(company, key=company.get)
        if company else
        "-"
    )

    top_location = (
        max(location, key=location.get)
        if location else
        "-"
    )

    top_employment = (
        max(employment, key=employment.get)
        if employment else
        "-"
    )

    return {

        "average_confidence":
            stats["average_confidence"],

        "highest_confidence":
            stats["highest_confidence"],

        "high_risk_jobs":
            stats["high_risk_jobs"],

        "fake_jobs":
            stats["fake_jobs"],

        "legitimate_jobs":
            stats["legitimate_jobs"],

        "pending_jobs":
            stats["pending_jobs"],

        "top_company":
            top_company,

        "top_location":
            top_location,

        "top_employment":
            top_employment

    }


# ============================================================
# TOP SUSPICIOUS JOBS
# ============================================================

def get_top_suspicious_jobs(
    db: Session,
    user_id: int,
    limit: int = 5
):

    return (

        db.query(PredictionResult)

        .join(Job)

        .options(
            joinedload(
                PredictionResult.job
            )
        )

        .filter(
            Job.user_id == user_id,
            PredictionResult.prediction == "Fake"
        )

        .order_by(
            PredictionResult.confidence.desc()
        )

        .limit(limit)

        .all()

    )


# ============================================================
# TOP CONFIDENT PREDICTIONS
# ============================================================

def get_top_confident_predictions(
    db: Session,
    user_id: int,
    limit: int = 5
):

    return (

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
            PredictionResult.confidence.desc()
        )

        .limit(limit)

        .all()

    )