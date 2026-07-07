from src.preprocessing import combine_job_fields


SUSPICIOUS_TERMS = {
    "bank details": 22,
    "bank account": 18,
    "transfer money": 24,
    "transfer client funds": 24,
    "crypto wallet": 22,
    "verification tokens": 18,
    "buy": 8,
    "no experience": 10,
    "start immediately": 10,
    "daily pay": 8,
    "earn $": 8,
    "$5000": 12,
    "personal wallet": 18,
    "confidential": 6,
}

TRUST_SIGNALS = {
    "health insurance": -5,
    "401k": -4,
    "requirements": -2,
    "bachelor": -3,
    "experience": -2,
    "training budget": -3,
    "medical": -4,
    "dental": -3,
}


def predict_job(job: dict) -> dict:
    text = combine_job_fields(job)
    score = 18
    reasons = []

    for term, weight in SUSPICIOUS_TERMS.items():
        if term in text:
            score += weight
            reasons.append(f"Suspicious phrase found: '{term}'")

    for term, weight in TRUST_SIGNALS.items():
        if term in text:
            score += weight

    if job.get("company", "").strip().lower() in {"confidential", "private recruiter"}:
        score += 12
        reasons.append("Company identity is vague or unverifiable.")

    if job.get("location", "").strip().lower() == "remote":
        score += 4

    if not job.get("salary_range", "").strip():
        score += 5
        reasons.append("Salary range is missing.")

    score = max(1, min(99, score))
    prediction = "Fake" if score >= 50 else "Legitimate"
    risk_level = "High" if score >= 70 else "Medium" if score >= 50 else "Low"

    if not reasons:
        reasons.append("Posting has ordinary role, company, and responsibility signals.")

    return {
        "prediction": prediction,
        "confidence": score if prediction == "Fake" else 100 - score,
        "risk_level": risk_level,
        "risk_score": score,
        "reasons": reasons,
    }
