from pydantic import BaseModel


class PredictionRequest(BaseModel):

    title: str
    company: str
    location: str | None = None
    department: str | None = None
    salary_range: str | None = None
    company_profile: str | None = None
    description: str
    requirements: str | None = None
    benefits: str | None = None

    telecommuting: bool
    has_company_logo: bool
    has_questions: bool

    employment_type: str | None = None
    required_experience: str | None = None
    required_education: str | None = None

    industry: str | None = None
    function: str | None = None


class PredictionResponse(BaseModel):

    prediction: str
    confidence: float