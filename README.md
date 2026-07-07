# Fake Job Posting Detection System

Streamlit prototype for AIMLCZG546 - Software Engineering for Machine Learning, Assignment I.

## Problem Statement

Online job platforms receive postings from many sources. Some postings are fraudulent and attempt to collect personal information, money, or bank details from applicants. This project implements an ML-inspired fake job detection prototype that classifies job postings as `Fake` or `Legitimate` and explains important risk signals.

## Features

- Single job prediction form.
- Batch CSV upload and analysis.
- Prediction distribution and risk charts.
- Explanation of suspicious signals.
- Architecture and pattern explanation in the app.

## Run Locally

```bash
cd assignment_streamlit_app
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## CSV Format

The batch workflow expects:

```text
title, company, location, employment_type, salary_range, description
```

Use `data/sample_jobs.csv` as the sample input.

## Architectural Patterns

1. CQRS Pattern
2. Microservices Pattern
3. Pipe-and-Filter Pattern

Details are available in `docs/assignment_report.md`.
