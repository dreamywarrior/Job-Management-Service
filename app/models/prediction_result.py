from datetime import datetime

from sqlalchemy import (
    String,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id"),
        nullable=False
    )

    prediction: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    predicted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    job = relationship(
        "Job",
        back_populates="predictions"
    )