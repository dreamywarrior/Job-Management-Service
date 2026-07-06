import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.user import User
from app.models.job import Job
from app.core.database import Base
from app.services.prediction_service import predict_job

# Dummy job data
jobs_data = [
    {
        "title": "Senior Python Developer",
        "company": "Tech Innovators Inc.",
        "description": "We are looking for an experienced Python developer with a strong background in FastAPI and SQLAlchemy. You will be building scalable backend services.",
        "location": "San Francisco, CA",
        "employment_type": "Full-time"
    },
    {
        "title": "IC&E Technician",
        "company": "Confidential",
        "description": "IC&amp;E Technician | Bakersfield, CA Mt. PosoPrincipal Duties and Responsibilities: Calibrates, tests, maintains, troubleshoots, and installs all power plant instrumentation, control systems and electrical equipment.Performs maintenance on motor control centers, motor operated valves, generators, excitation equipment and motors.Performs preventive, predictive and corrective maintenance on equipment, coordinating work with various team members.",
        "location": "Bakersfield, CA",
        "employment_type": "Full-time"
    },
    {
        "title": "Data Entry Clerk",
        "company": "Global Data Solutions",
        "description": "Earn $5000 a week working from home! No experience needed! Just send us your bank details to get started immediately. Must be willing to transfer money.",
        "location": "Remote",
        "employment_type": "Contract"
    },
    {
        "title": "Forward Cap.",
        "company": "Forward Cap.",
        "description": "The group has raised a fund for the purchase of homes in the Southeast. The student on this project will help them build their investments from the ground up and will help with the analysis and modeling of their investments. We should be looking for someone with a strong general finance skills and has a lot of entrepreneurial ability.",
        "location": "Remote",
        "employment_type": "Part-time"
    }
]

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check for a user
    user = db.query(User).first()
    if not user:
        print("Creating a dummy user...")
        user = User(
            full_name="Test User",
            email="test@example.com",
            password_hash="dummy_hash"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    print(f"Using user: {user.email} (ID: {user.id})")
    
    # Create jobs
    for data in jobs_data:
        job = Job(
            user_id=user.id,
            title=data["title"],
            company=data["company"],
            description=data["description"],
            location=data["location"],
            employment_type=data["employment_type"]
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        print(f"Created job: {job.title}")
        
        # Run prediction
        predict_job(db, job)
        print("  -> Prediction generated.")
        
    db.close()
    print("Dummy data seeding complete!")

if __name__ == "__main__":
    seed()
