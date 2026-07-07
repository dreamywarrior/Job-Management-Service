from datetime import datetime, timedelta

from pwdlib import PasswordHash

from app.core.database import Base, SessionLocal, engine
from app.models.job import Job
from app.models.prediction_result import PredictionResult
from app.models.user import User
from app.services.prediction_service import predict_job

password_hash = PasswordHash.recommended()
now = datetime.now()

jobs_data = [
    {
        "title": "Senior Python Developer",
        "company": "Northstar Labs",
        "description": "Build FastAPI services, background jobs, and SQLAlchemy-backed APIs for hiring workflow products.",
        "location": "San Francisco, CA",
        "department": "Engineering",
        "salary_range": "$135,000-$165,000",
        "company_profile": "Product engineering company building workflow tools for hiring teams.",
        "requirements": "5+ years Python, REST APIs, SQLAlchemy, cloud deployment.",
        "benefits": "Health insurance, 401k match, learning budget, flexible PTO.",
        "telecommuting": True,
        "has_company_logo": True,
        "has_questions": True,
        "employment_type": "Full-time",
        "required_experience": "Mid-Senior level",
        "required_education": "Bachelor's Degree",
        "industry": "Computer Software",
        "function": "Engineering",
        "application_deadline": now + timedelta(days=14),
        "job_link": "https://example.com/jobs/senior-python-developer",
    },
    {
        "title": "IC&E Technician",
        "company": "Valley Energy Partners",
        "description": "Calibrate, test, maintain, troubleshoot, and install plant instrumentation, control systems, and electrical equipment.",
        "location": "Bakersfield, CA",
        "department": "Operations",
        "salary_range": "$38-$46/hour",
        "company_profile": "Regional energy operator focused on reliable plant operations.",
        "requirements": "Instrumentation experience, electrical safety knowledge, shift availability.",
        "benefits": "Medical, dental, overtime eligibility, safety training.",
        "telecommuting": False,
        "has_company_logo": True,
        "has_questions": True,
        "employment_type": "Full-time",
        "required_experience": "Associate",
        "required_education": "Vocational",
        "industry": "Oil & Energy",
        "function": "Technician",
        "application_deadline": now + timedelta(days=3),
        "job_link": "https://example.com/jobs/ice-technician",
    },
    {
        "title": "Data Entry Clerk",
        "company": "Global Data Solutions",
        "description": "Earn $5000 a week working from home. No experience needed. Send bank details to start immediately and transfer client funds.",
        "location": "Remote",
        "department": "Administration",
        "salary_range": "$5,000/week",
        "company_profile": "",
        "requirements": "No experience required. Must have personal bank account.",
        "benefits": "Immediate payment, flexible hours.",
        "telecommuting": True,
        "has_company_logo": False,
        "has_questions": False,
        "employment_type": "Contract",
        "required_experience": "Entry level",
        "required_education": "Unspecified",
        "industry": "Administrative",
        "function": "Data Entry",
        "application_deadline": now + timedelta(hours=8),
        "job_link": "https://example.com/jobs/data-entry-clerk",
    },
    {
        "title": "Forward Cap.",
        "company": "Forward Cap.",
        "description": "The group has raised a fund for the purchase of homes in the Southeast. The student on this project will help them build their investments from the ground up and will help with the analysis and modeling of their investments. We should be looking for someone with a strong general finance skills and has a lot of entrepreneurial ability.",
        "location": "Remote",
        "employment_type": "Part-time",
        "application_deadline": now + timedelta(days=4),
        "job_link": "https://example.com/jobs/forward-cap",
    },
    {
        "title": "IC&E Technician Mt Poso",
        "company": "Refined Resources",
        "description": "IC&E Technician | Bakersfield, CA Mt. Poso Principal Duties and Responsibilities: Calibrates, tests, maintains, troubleshoots, and installs all power plant instrumentation, control systems and electrical equipment.",
        "location": "US, CA, Bakersfield, CA / Mt. Poso",
        "employment_type": "Full-time",
        "application_deadline": now + timedelta(days=5),
        "job_link": "https://example.com/jobs/ic-and-e-technician-mt-poso",
    },
    {
        "title": "Financing Auto(car) Sales",
        "company": "Hazelcrest Motors",
        "description": "Looking for adventurous people to join a thriving industry. We offer training and competitive earnings. From $500 to $1000 a week by contract.",
        "location": "US, IL, Hazelcrest",
        "employment_type": "Contract",
        "application_deadline": now + timedelta(days=6),
        "job_link": "https://example.com/jobs/financing-auto-sales",
    },
    {
        "title": "Administrative Assistant",
        "company": "Elite Support Group",
        "description": "As an Administrative Assistant, you will manage incoming and outgoing communication, multiple calendars, invoices, and travel arrangements. Starting pay $25/hr.",
        "location": "US, CA, Los Angeles",
        "employment_type": "Full-time",
        "application_deadline": now + timedelta(days=7),
        "job_link": "https://example.com/jobs/administrative-assistant",
    },
    {
        "title": "Sales Executive",
        "company": "Karachi Trade Hub",
        "description": "Sales Executive position with amazing earnings, contract work, and immediate start. Apply today for fast onboarding and weekly pay.",
        "location": "PK, SD, Karachi",
        "employment_type": "Contract",
        "application_deadline": now + timedelta(days=8),
        "job_link": "https://example.com/jobs/sales-executive",
    },
    {
        "title": "Technical & Customer Support Associates",
        "company": "Accion Finance",
        "description": "Interface with customers via inbound or outbound calls to resolve issues. Flexible shifts, excellent benefits, and inbound calls only.",
        "location": "US, PA, Philadelphia",
        "employment_type": "Full-time",
        "application_deadline": now + timedelta(days=9),
        "job_link": "https://example.com/jobs/technical-customer-support-associates",
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("Wiping existing data...")
    db.query(PredictionResult).delete()
    db.query(Job).delete()
    db.query(User).delete()
    db.commit()

    print("Creating a test user...")
    user = User(
        full_name="Test User",
        email="test@example.com",
        password_hash=password_hash.hash("testpassword"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    print(f"Using user: {user.email} (ID: {user.id})")

    for data in jobs_data:
        job = Job(user_id=user.id, **data)
        db.add(job)
        db.commit()
        db.refresh(job)
        print(f"Created job: {job.title}")
        predict_job(db, job)
        print("  -> Prediction generated.")

    db.close()
    print("Trimmed dummy data seeding complete!")


if __name__ == "__main__":
    seed()
