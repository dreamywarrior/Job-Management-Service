# Documentation: Fraud Prediction Service (Query Side)

**Branch:** implementation_version_2

## 1. Overview
This document outlines the implementation of the Query Side of the Job Management Service, utilizing the **CQRS (Command Query Responsibility Segregation)** architectural pattern. While the Command side handles the creation and modification of job postings, this implementation focuses on the Query side: analyzing the data, running Machine Learning inference to detect fraudulent jobs, and visualizing the analytics.

## 2. Setup Instructions

To run the complete application locally, follow these steps:

### Prerequisites
Ensure you have Python 3.9+ installed.

### Installation
1. Navigate to the project root directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Training the Machine Learning Model
Before running the application, you must train the Random Forest model so the prediction service has a model to load.
1. Run the training script:
   ```bash
   python ml/train_model.py
   ```
2. Wait for the dataset to download and train. You should see an accuracy score printed to the console, and a `ml/model.pkl` file will be generated.

### Seeding the Database (Optional but Recommended)
To populate the application with dummy data for testing and analytics visualization:
```bash
python seed_db.py
```

### Running the Server
Start the FastAPI server using Uvicorn:
```bash
uvicorn app.main:app --reload
```
Access the application at `http://127.0.0.1:8000`.

## 3. Testing the Application

### Manual UI Testing
1. **Login/Register:** Open the app and create a test account (or login as `test@example.com` if you seeded the database).
2. **Add a Job (Command):** Navigate to "Add New Job". Input a suspicious description (e.g., "Earn $5000 a week stuffing envelopes, no experience needed, wire transfer fee required.")
3. **Verify Job (Query):** Go to "My Jobs", select the job you just created, and click "Verify Job".
4. **View Prediction:** You will be routed to the Prediction Result page. The ML model will analyze the text and return a "Fake" or "Legitimate" tag along with a Confidence Score.
5. **View Analytics:** Navigate to the Dashboard to see the Fraud Analytics pie chart update in real-time based on your prediction history.

## 4. System Architecture

The system utilizes a hybrid approach combining **Layered (MVC) Architecture** with **CQRS**:

### The Core Concept: CQRS
CQRS is a pattern that splits our application into two completely separate "lanes": one lane strictly for **Writing** data (Command), and the other strictly for **Reading/Analyzing** data (Query).

Here is a visual flowchart of how the two lanes operate:

```text
========================================================================
                      LANE 1: COMMAND SIDE (implementation_version_1)
========================================================================

  [ USER ] ---> Clicks "Add Job" on the website
                  |
                  v
          [ jobs.py Router ] ---> Receives the raw text data
                  |
                  v
       [ SQLite Database ] <--- Saves the job posting securely


========================================================================
                      LANE 2: QUERY & ML SIDE (implementation_version_2)
========================================================================

  [ USER ] ---> Clicks "Verify Job" on their dashboard
                  |
                  v
       [ prediction.py Router ] ---> Asks the database for that specific job
                  |
                  v
    [ prediction_service.py ] ---> Wakes up the Machine Learning Model
                  |
                  v
         [ ml/model.pkl ] ---> Analyzes text & returns "Fake" or "Legitimate"
                  |
                  v
       [ SQLite Database ] <--- Saves the final Prediction Result
                  |
                  v
  [ USER ] <--- Website displays the Confidence Score and Updates Charts
```

### Plain English Breakdown

**Lane 1: The Command Side (implementation_version_1)**
*   **Goal:** Get data into the system safely.
*   **How it works:** When a user fills out the "Add New Job" form, the website sends that data to the **Command Router** (`jobs.py`). The router's only job is to take that raw text and save it directly into the database. It doesn't analyze it; it just stores it.

**Lane 2: The Query & ML Side (implementation_version_2)**
*   **Goal:** Read the data, run the AI, and show the results.
*   **How it works:** When a user clicks the "Verify Job" button, they trigger the **Query Router** (`prediction.py`). This router grabs the text of that specific job from the database and hands it to the **Prediction Service**. The service feeds the text into the **Machine Learning Engine** (`model.pkl`), which calculates the math and hands back an answer (e.g., *"This is Fake with 92% confidence"*). The service saves that answer to the database for history and displays it on the user's screen.

*   **Command Side (implementation_version_1):** Routes in `jobs.py` interact with `job_service.py` to handle write operations (Create, Update, Delete) to the SQLite database using SQLAlchemy ORM.
*   **Query Side (implementation_version_2):** 
    *   Routes in `prediction.py` and `dashboard.py` handle read operations.
    *   The `prediction_service.py` acts as the bridge to the Machine Learning model (`model.pkl`). 
    *   Instead of writing raw data, it queries existing job postings, extracts text features, and passes them to the ML pipeline for read-only inference.
    *   The results are then persisted in a separate `PredictionResult` table, strictly segregating the analytical data from the core `Job` transactional data.

## 5. Modular Explanation

### `ml/train_model.py` (The ML Engine)
*   **Data Ingestion:** Downloads the EMSCAD Fake Job Posting dataset via pandas.
*   **Preprocessing:** Combines the `title` and `description` fields. Uses `TfidfVectorizer` (Term Frequency-Inverse Document Frequency) to convert raw text into numerical feature vectors, capping at the top 5000 features.
*   **Training:** Fits a `RandomForestClassifier` with 100 estimators.
*   **Serialization:** Uses `joblib` to export the trained pipeline as `model.pkl`.

### `app/services/prediction_service.py` (The Inference Bridge)
*   **Global Loading:** Loads `model.pkl` into memory at the module level when the server starts. This prevents the heavy operation of loading the model during every user request.
*   **`predict_job()`:** Takes a database session and a `Job` object. It extracts the title and description, feeds it into the loaded ML pipeline, and extracts both the predicted class (Fake/Legitimate) and the mathematical probability (`predict_proba`) to generate a user-friendly Confidence Score. It then saves this result to the database.

### `app/routers/prediction.py` (The API Layer)
*   Exposes the `/{job_id}` endpoint which triggers the prediction service.
*   Exposes the `/history` endpoint which queries the database for all past predictions made by the logged-in user.

### `app/templates/dashboard.html` (The Visualization Layer)
*   Utilizes **Chart.js** to render a client-side pie chart.
*   Reads Jinja2 injected variables (`fake_jobs`, `legitimate_jobs`) provided by the `dashboard_service.py` to dynamically visualize the ratio of fraudulent postings identified by the system.
