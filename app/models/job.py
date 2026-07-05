from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    company: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    location: Mapped[str | None] = mapped_column(String(150))

    department: Mapped[str | None] = mapped_column(String(150))

    salary_range: Mapped[str | None] = mapped_column(String(100))

    company_profile: Mapped[str | None] = mapped_column(Text)

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    requirements: Mapped[str | None] = mapped_column(Text)

    benefits: Mapped[str | None] = mapped_column(Text)

    telecommuting: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    has_company_logo: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    has_questions: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    employment_type: Mapped[str | None] = mapped_column(String(100))

    required_experience: Mapped[str | None] = mapped_column(String(100))

    required_education: Mapped[str | None] = mapped_column(String(100))

    industry: Mapped[str | None] = mapped_column(String(100))

    function: Mapped[str | None] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    owner = relationship(
        "User",
        back_populates="jobs"
    )

    prediction_result = relationship(
        "PredictionResult",
        back_populates="job",
        uselist=False,
        cascade="all, delete-orphan"
    )