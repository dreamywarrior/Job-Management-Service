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
        "title": "Investment Analyst Intern",
        "company": "Forward Capital Group",
        "description": "Support acquisition analysis, financial modeling, and market research for residential investment opportunities.",
        "location": "Remote",
        "department": "Finance",
        "salary_range": "$22-$28/hour",
        "company_profile": "Real estate investment group focused on residential acquisitions.",
        "requirements": "Excel modeling, finance coursework, strong writing skills.",
        "benefits": "Mentorship, flexible schedule, project-based bonus.",
        "telecommuting": True,
        "has_company_logo": True,
        "has_questions": True,
        "employment_type": "Part-time",
        "required_experience": "Internship",
        "required_education": "Some College",
        "industry": "Real Estate",
        "function": "Finance",
        "application_deadline": now + timedelta(days=21),
        "job_link": "https://example.com/jobs/investment-analyst-intern",
    },
    {
        "title": "UX Designer",
        "company": "PixelBridge Studio",
        "description": "Design research-backed dashboards, wireframes, prototypes, and usability improvements for SaaS customers.",
        "location": "Austin, TX",
        "department": "Design",
        "salary_range": "$92,000-$118,000",
        "company_profile": "Design studio partnering with B2B product teams.",
        "requirements": "Portfolio, Figma, user research, design systems.",
        "benefits": "Hybrid schedule, health insurance, conference budget.",
        "telecommuting": False,
        "has_company_logo": True,
        "has_questions": True,
        "employment_type": "Full-time",
        "required_experience": "Mid level",
        "required_education": "Bachelor's Degree",
        "industry": "Design",
        "function": "Design",
        "application_deadline": now + timedelta(days=10),
        "job_link": "https://example.com/jobs/ux-designer",
    },
    {
        "title": "Customer Support Specialist",
        "company": "CareCloud Health",
        "description": "Respond to customer tickets, document product issues, and coordinate with engineering for healthcare platform users.",
        "location": "Chicago, IL",
        "department": "Customer Success",
        "salary_range": "$48,000-$58,000",
        "company_profile": "Healthcare SaaS company serving clinics and care teams.",
        "requirements": "Customer support experience, clear communication, CRM familiarity.",
        "benefits": "Medical, dental, paid holidays, wellness stipend.",
        "telecommuting": False,
        "has_company_logo": True,
        "has_questions": True,
        "employment_type": "Full-time",
        "required_experience": "Associate",
        "required_education": "High School",
        "industry": "Healthcare",
        "function": "Customer Service",
        "application_deadline": now + timedelta(days=5),
        "job_link": "https://example.com/jobs/customer-support-specialist",
    },
    {
        "title": "Crypto Payroll Assistant",
        "company": "Private Recruiter",
        "description": "Process payroll from your personal wallet. Training provided. Must buy verification tokens before onboarding.",
        "location": "Remote",
        "department": "Payroll",
        "salary_range": "$90/hour",
        "company_profile": "",
        "requirements": "Personal crypto wallet, ability to start today.",
        "benefits": "Daily pay.",
        "telecommuting": True,
        "has_company_logo": False,
        "has_questions": False,
        "employment_type": "Temporary",
        "required_experience": "Not Applicable",
        "required_education": "Unspecified",
        "industry": "Financial Services",
        "function": "Accounting",
        "application_deadline": now + timedelta(hours=20),
        "job_link": "https://example.com/jobs/crypto-payroll-assistant",
    },
    {
        "title": "Marketing Coordinator",
        "company": "BrightWave Retail",
        "description": "Coordinate email campaigns, retail promotions, social reporting, and launch calendars across regional stores.",
        "location": "New York, NY",
        "department": "Marketing",
        "salary_range": "$62,000-$74,000",
        "company_profile": "Retail brand with digital and store channels across the US.",
        "requirements": "Campaign coordination, analytics basics, copywriting.",
        "benefits": "Commuter benefits, employee discount, paid time off.",
        "telecommuting": False,
        "has_company_logo": True,
        "has_questions": True,
        "employment_type": "Full-time",
        "required_experience": "Associate",
        "required_education": "Bachelor's Degree",
        "industry": "Retail",
        "function": "Marketing",
        "application_deadline": now + timedelta(days=18),
        "job_link": "https://example.com/jobs/marketing-coordinator",
    },
    {
        "title": "Warehouse Operations Lead",
        "company": "MetroShip Logistics",
        "description": "Lead receiving, inventory counts, safety checks, and daily dispatch coordination in a fast-moving warehouse.",
        "location": "Dallas, TX",
        "department": "Logistics",
        "salary_range": "$58,000-$68,000",
        "company_profile": "Third-party logistics provider for consumer goods brands.",
        "requirements": "Warehouse leadership, WMS experience, forklift certification preferred.",
        "benefits": "Health insurance, shift differential, paid training.",
        "telecommuting": False,
        "has_company_logo": True,
        "has_questions": True,
        "employment_type": "Full-time",
        "required_experience": "Mid level",
        "required_education": "High School",
        "industry": "Logistics",
        "function": "Operations",
        "application_deadline": now + timedelta(days=7),
        "job_link": "https://example.com/jobs/warehouse-operations-lead",
    },
    {
        "title": "Junior QA Tester",
        "company": "AppForge Systems",
        "description": "Create manual test cases, run regression tests, log defects, and support release validation for web applications.",
        "location": "Seattle, WA",
        "department": "Quality Assurance",
        "salary_range": "$55,000-$70,000",
        "company_profile": "Software consultancy building internal tools and customer portals.",
        "requirements": "Attention to detail, test case writing, basic SQL helpful.",
        "benefits": "Remote Fridays, training budget, medical coverage.",
        "telecommuting": True,
        "has_company_logo": True,
        "has_questions": True,
        "employment_type": "Full-time",
        "required_experience": "Entry level",
        "required_education": "Associate Degree",
        "industry": "Information Technology",
        "function": "Quality Assurance",
        "application_deadline": now + timedelta(days=12),
        "job_link": "https://example.com/jobs/junior-qa-tester",
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
    print("Diversified dummy data seeding complete!")


if __name__ == "__main__":
    seed()
