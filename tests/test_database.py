from app.core.database import SessionLocal
from app.models.user import User
from app.models.job import Job
from app.models.prediction_result import PredictionResult


def test_database():

    db = SessionLocal()

    try:

        print("=" * 50)
        print("Testing Database CRUD")
        print("=" * 50)

        # ------------------------
        # Create User
        # ------------------------

        user = User(
            full_name="Vish",
            email="vish@example.com",
            password_hash="hashed_password"
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"User Created: {user.id}")

        # ------------------------
        # Create Job
        # ------------------------

        job = Job(
            user_id=user.id,
            title="Software Engineer",
            company="Google",
            location="Bangalore",
            department="Engineering",
            salary_range="15-20 LPA",
            company_profile="Google India",
            description="Hiring Backend Engineers",
            requirements="Python, SQL",
            benefits="Medical Insurance",
            telecommuting=False,
            has_company_logo=True,
            has_questions=True,
            employment_type="Full-time",
            required_experience="2-4 years",
            required_education="Bachelor's",
            industry="IT",
            function="Engineering"
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        print(f"Job Created: {job.id}")

        # ------------------------
        # Create Prediction
        # ------------------------

        prediction = PredictionResult(
            job_id=job.id,
            prediction="Legitimate",
            confidence=0.96
        )

        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        print(f"Prediction Created: {prediction.id}")

        # ------------------------
        # Read
        # ------------------------

        jobs = db.query(Job).all()

        print()

        print("Jobs in Database")

        for job in jobs:
            print(job.title, "-", job.company)

        # ------------------------
        # Update
        # ------------------------

        job.company = "Google India"

        db.commit()

        print()

        print("Job Updated")

        # ------------------------
        # Delete Prediction
        # ------------------------

        db.delete(prediction)

        db.commit()

        print("Prediction Deleted")

        print()

        print("CRUD Test Successful")

    finally:

        db.close()


if __name__ == "__main__":
    test_database()