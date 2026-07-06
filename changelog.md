# Changelog: Updates in implementation_version_2

This document details the components and features added to complete the application, transforming it from a structural shell (implementation_version_1) into a fully functional Machine Learning integrated system (implementation_version_2).

## 1. Machine Learning Engine (New)
*   **Initial State:** No machine learning capability.
*   **Added:** 
    *   Created `ml/train_model.py`, a complete ML pipeline.
    *   The script automatically downloads the **EMSCAD Fake Job Posting Dataset** (~17,000 real-world job postings).
    *   Implemented a text processing pipeline using `TfidfVectorizer` to extract features from job titles and descriptions.
    *   Trained a `RandomForestClassifier` which achieved a **~97.8% accuracy** on the test split.
    *   The trained model is serialized and saved as `ml/model.pkl`.
    *   Updated `requirements.txt` with `pandas`, `scikit-learn`, and `joblib`.

## 2. Prediction API & Inference Integration (Upgraded)
*   **Initial State:** `prediction_service.py` contained placeholder logic, returning a random choice of "Fake" or "Legitimate" using Python's `random` module.
*   **Added:** 
    *   Refactored `app/services/prediction_service.py` to load the serialized `model.pkl` file globally when the server starts.
    *   When the "Verify Job" endpoint is triggered, the service now feeds the actual job title and description text into the Random Forest model for inference.
    *   The model returns a mathematically calculated classification and a true probability score, which is then mapped to the Confidence percentage.

## 3. Fraud Analytics Visualization (New)
*   **Initial State:** The `dashboard.html` template only showed raw numerical counters (e.g., "Fake Jobs: 3"). The "Analytics Dashboard" requirement for the Query side was unfulfilled.
*   **Added:** 
    *   Integrated the **Chart.js** library into `app/templates/dashboard.html`.
    *   Added a dynamic Pie Chart to the dashboard that visually breaks down the proportion of Fake vs. Legitimate jobs based on the user's actual prediction history.

## 4. Database Seeding Tool (New)
*   **Initial State:** The database was empty upon initialization, making testing and final report screenshot generation difficult.
*   **Added:** 
    *   Created `seed_db.py`, a Python script that programmatically populates the database.
    *   It generates a test user and inserts a mix of realistic legitimate jobs and known fake jobs (extracted directly from the EMSCAD dataset).
    *   It automatically runs these jobs through the prediction service to populate the history and analytics charts for immediate viewing.
