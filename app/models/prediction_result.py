from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class PredictionResult(Base):
    __tablename__ = "prediction_results"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================================
    # Foreign Key
    # =====================================================

    job_id = Column(
        Integer,
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    # =====================================================
    # ML Prediction
    # =====================================================

    prediction = Column(
        String(30),
        nullable=False
    )

    confidence = Column(
        Float,
        nullable=False,
        default=0.0
    )

    # =====================================================
    # NEW : Risk Level
    # =====================================================

    risk_level = Column(
        String(20),
        nullable=False,
        default="Unknown"
    )

    # =====================================================
    # NEW : Model Used
    # =====================================================

    model_used = Column(
        String(100),
        nullable=False,
        default="Random Forest + TF-IDF v1.0"
    )

    # =====================================================
    # NEW : Prediction Explanation
    # =====================================================

    explanation = Column(
        Text,
        nullable=True
    )

    # =====================================================
    # Prediction Timestamp
    # =====================================================

    predicted_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # =====================================================
    # Relationship
    # =====================================================

    job = relationship(
        "Job",
        back_populates="prediction_result"
    )

    # =====================================================
    # Helper Properties
    # =====================================================

    @property
    def confidence_percentage(self):
        """
        Returns confidence formatted with %
        """
        return f"{self.confidence:.2f}%"

    @property
    def badge_color(self):
        """
        Bootstrap badge color
        """

        mapping = {
            "Legitimate": "success",
            "Fake": "danger",
            "Pending": "warning"
        }

        return mapping.get(
            self.prediction,
            "secondary"
        )

    @property
    def risk_badge(self):
        """
        Bootstrap badge color for risk level
        """

        mapping = {
            "Low": "success",
            "Medium": "warning",
            "High": "danger",
            "Very High": "dark",
            "Unknown": "secondary"
        }

        return mapping.get(
            self.risk_level,
            "secondary"
        )

    def __repr__(self):

        return (
            f"<PredictionResult("
            f"id={self.id}, "
            f"prediction='{self.prediction}', "
            f"confidence={self.confidence}, "
            f"risk='{self.risk_level}')>"
        )