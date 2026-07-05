from app.core.database import Base, engine

# Import all models
from app.models.user import User
from app.models.job import Job
from app.models.prediction_result import PredictionResult


def init_database():
    print("Creating database...")

    Base.metadata.create_all(bind=engine)

    print("Database created successfully!")


if __name__ == "__main__":
    init_database()