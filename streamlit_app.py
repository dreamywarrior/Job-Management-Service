from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.database import SessionLocal
from app.init_db import init_database
from app.schemas.job import JobCreate
from app.services.job_service import create_job
from app.services.prediction_service import get_prediction_history, predict_job

st.set_page_config(page_title="Fake Job Detection", page_icon="🛡️", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(252,175,69,.16), transparent 28rem),
            radial-gradient(circle at top right, rgba(225,48,108,.12), transparent 26rem),
            #fafafa;
    }
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #dbdbdb;
    }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dbdbdb;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 8px 28px rgba(0,0,0,.06);
    }
    .hero {
        padding: 28px 32px;
        border-radius: 20px;
        color: white;
        background: linear-gradient(135deg,#405de6,#833ab4,#c13584,#e1306c,#fcaf45);
        margin-bottom: 24px;
    }
    .hero h1 { margin: 0; font-size: 38px; }
    .hero p { margin: 8px 0 0; opacity: .92; font-size: 17px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_db():
    return SessionLocal()


def ensure_database_and_user():
    init_database()
    st.session_state.user_id = 1


def job_payload_from_form():
    return JobCreate(
        title=st.session_state.title,
        company=st.session_state.company,
        location=st.session_state.location or "",
        department=st.session_state.department or "",
        salary_range=st.session_state.salary_range or "",
        company_profile=st.session_state.company_profile or "",
        description=st.session_state.description,
        requirements=st.session_state.requirements or "",
        benefits=st.session_state.benefits or "",
        telecommuting=st.session_state.telecommuting,
        has_company_logo=st.session_state.has_company_logo,
        has_questions=st.session_state.has_questions,
        employment_type=st.session_state.employment_type,
        required_experience=st.session_state.required_experience or "",
        required_education=st.session_state.required_education or "",
        industry=st.session_state.industry or "",
        function=st.session_state.function or "",
        application_deadline=None,
        job_link=st.session_state.job_link or None,
    )


def submit_prediction():
    db = get_db()
    try:
        job = create_job(db=db, job=job_payload_from_form(), user_id=st.session_state.user_id)
        prediction = predict_job(db, job)
        st.session_state.last_result = {
            "job_title": job.title,
            "prediction": prediction.prediction,
            "confidence": prediction.confidence,
            "risk_level": prediction.risk_level,
            "explanation": prediction.explanation,
        }
        st.success("Prediction saved to history.")
    finally:
        db.close()


def load_history():
    db = get_db()
    try:
        return get_prediction_history(db, st.session_state.user_id)
    finally:
        db.close()


def render_history(history):
    st.subheader("Prediction History")
    if not history:
        st.info("No prediction history yet. Submit a job above and it will appear here.")
        return
    rows = []
    for item in history:
        rows.append(
            {
                "Job": item.job.title,
                "Company": item.job.company,
                "Prediction": item.prediction,
                "Confidence": round(float(item.confidence), 2),
                "Risk": item.risk_level,
                "Predicted At": item.predicted_at.strftime("%d %b %Y %I:%M %p"),
                "Explanation": item.explanation or "",
            }
        )
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.plotly_chart(px.pie(df, names="Prediction", title="Prediction Distribution"), use_container_width=True)


ensure_database_and_user()
st.sidebar.subheader("Saved History")
st.sidebar.caption("All predictions are saved in the shared job database.")

st.markdown(
    """
    <div class="hero">
        <h1>Fake Job Posting Detection System</h1>
        <p>Submit a job posting, save the prediction, and review your full prediction history.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

mode = st.sidebar.radio("Select workflow", ["Single Prediction", "Batch Analysis", "Architecture"])

if mode == "Single Prediction":
    left, right = st.columns([1.15, 0.85])
    with left:
        st.subheader("Job Submission")
        with st.form("job_form"):
            st.text_input("Job Title", value="Data Entry Clerk", key="title")
            st.text_input("Company", value="Global Data Solutions", key="company")
            st.text_input("Location", value="Remote", key="location")
            st.text_input("Department", value="Operations", key="department")
            st.text_input("Salary Range", value="$5,000/week", key="salary_range")
            st.text_area("Company Profile", value="", height=90, key="company_profile")
            st.text_area(
                "Description",
                value="Earn $5000 a week working from home. No experience needed. Send bank details to get started immediately.",
                height=160,
                key="description",
            )
            st.text_area("Requirements", value="", height=90, key="requirements")
            st.text_area("Benefits", value="", height=90, key="benefits")
            st.checkbox("Telecommuting", value=True, key="telecommuting")
            st.checkbox("Has Company Logo", value=False, key="has_company_logo")
            st.checkbox("Has Questions", value=False, key="has_questions")
            st.text_input("Employment Type", value="Contract", key="employment_type")
            st.text_input("Required Experience", value="Entry level", key="required_experience")
            st.text_input("Required Education", value="Unspecified", key="required_education")
            st.text_input("Industry", value="Administrative", key="industry")
            st.text_input("Function", value="Data Entry", key="function")
            st.text_input("Job Link", value="", key="job_link")
            submitted = st.form_submit_button("Submit for Prediction")
        if submitted:
            submit_prediction()

    with right:
        st.subheader("Latest Result")
        result = st.session_state.get("last_result")
        if result:
            st.metric("Prediction", result["prediction"])
            st.metric("Confidence", f"{result['confidence']}%")
            st.metric("Risk Level", result["risk_level"])
            st.progress(min(max(float(result["confidence"]) / 100, 0), 1))
            st.markdown("**Explanation**")
            st.write(result["explanation"] or "No explanation available.")
        else:
            st.info("Submit the form to generate and save a prediction.")

    st.markdown("---")
    render_history(load_history())

elif mode == "Batch Analysis":
    st.subheader("Batch CSV Analysis")
    st.write("Upload a CSV with title, company, location, employment_type, salary_range, and description columns.")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded:
        source_df = pd.read_csv(uploaded)
    else:
        source_df = pd.read_csv("data/sample_jobs.csv")
        st.info("Using bundled sample_jobs.csv. Upload your own file to replace it.")

    history_rows = []
    for _, row in source_df.fillna("").iterrows():
        db = get_db()
        try:
            job = create_job(
                db=db,
                job=JobCreate(
                    title=str(row.get("title", "")),
                    company=str(row.get("company", "")),
                    location=str(row.get("location", "")),
                    department="",
                    salary_range=str(row.get("salary_range", "")),
                    company_profile="",
                    description=str(row.get("description", "")),
                    requirements="",
                    benefits="",
                    telecommuting=str(row.get("location", "")).strip().lower() == "remote",
                    has_company_logo=False,
                    has_questions=False,
                    employment_type=str(row.get("employment_type", "")),
                    required_experience="",
                    required_education="",
                    industry="",
                    function="",
                    application_deadline=None,
                    job_link=None,
                ),
                user_id=st.session_state.user_id,
            )
            prediction = predict_job(db, job)
            history_rows.append(
                {
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "employment_type": job.employment_type,
                    "prediction": prediction.prediction,
                    "confidence": prediction.confidence,
                    "risk_level": prediction.risk_level,
                    "reasons": prediction.explanation,
                }
            )
        finally:
            db.close()

    result_df = pd.DataFrame(history_rows)
    if not result_df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Jobs", len(result_df))
        c2.metric("Fake Jobs", int((result_df["prediction"] == "Fake").sum()))
        c3.metric("Legitimate Jobs", int((result_df["prediction"] == "Legitimate").sum()))
        chart_left, chart_right = st.columns(2)
        with chart_left:
            st.plotly_chart(px.pie(result_df, names="prediction", title="Prediction Distribution"), use_container_width=True)
        with chart_right:
            st.plotly_chart(px.histogram(result_df, x="risk_level", color="prediction", title="Risk Level Distribution"), use_container_width=True)
        st.dataframe(result_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    render_history(load_history())

else:
    st.subheader("System Architecture and Patterns")
    st.markdown(
        """
        **CQRS Pattern**
        - Commands handle prediction submissions and persist them in the database.
        - Queries read the stored prediction history and summary data.

        **Microservices Pattern**
        - `PredictionService` in the FastAPI app handles trained-model inference and persistence.
        - `ReportingService` reads prediction history and analytics from the database.
        - The Streamlit app acts as a separate presentation client over the shared data/services.

        **Pipe-and-Filter Pattern**
        - Input job posting -> text normalization -> feature/signal extraction -> risk scoring -> prediction -> explanation.
        """
    )
