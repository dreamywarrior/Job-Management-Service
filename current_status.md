# Current Status: Fake Job Posting Detection System

## 1. Project Details

**Project Option:** Fake Job Posting Detection System
*   **Description:** Detects whether a job posting is genuine or fraudulent using an NLP-based ML model.
*   **Microservices:** User Service, Job Management Service, Fraud Prediction Service.
*   **Architecture Pattern:** CQRS (Command Query Responsibility Segregation)
    *   *Commands:* Register/Login, Add/Edit/Delete Job Posting, Report Prediction.
    *   *Queries:* Predict Fraud, View Prediction History, Search Job Postings, Fraud Analytics.

---

## 2. Task Split & Completion Status

The entire codebase is 100% finished. All remaining tasks are strictly documentation, diagrams, or taking screenshots for the final report. As **Person 4**, your entire workload is fully completed!

### Person 1 – Requirements Engineer
| Task | Description | Status | Notes |
| :--- | :--- | :--- | :--- |
| 1 | Select application domain | ✅ **Completed** | Fake Job Detection chosen. |
| 2 | Define problem statement | ⏳ **Pending** | Needs to be written in the report. |
| 3 | Requirement specifications | ⏳ **Pending** | Needs to be written in the report. |
| 4 | Measurable goals | ⏳ **Pending** | Needs to be written in the report. |
| 5 | Test the complete application for bugs/issues | ✅ **Completed** | UI and ML pipeline tested. |
| 6 | Report identified bugs to the implementation team | ✅ **Completed** | Fixed the dummy data prediction issue. |
| 7 | Take screenshots of the tested application for the final report | ⏳ **Pending** | Needs to screenshot the Dashboard, Add Job, and History pages. |

### Person 2 – ML Architect & Documentation
| Task | Description | Status | Notes |
| :--- | :--- | :--- | :--- |
| 1 | Business View (GR4ML) | ⏳ **Pending** | Documentation required. |
| 2 | Analytics Design View (GR4ML) | ⏳ **Pending** | Documentation required. |
| 3 | Data Preparation View (GR4ML) | ⏳ **Pending** | Documentation required. |
| 4 | Identify top 3 quality requirements with justification | ⏳ **Pending** | Documentation required. |
| 5 | Prepare and maintain the project documentation/report | ⏳ **Pending** | Must compile everyone's work into the final PDF/Word doc. |

### Person 3 – Software Architect & Developer
| Task | Description | Status | Notes |
| :--- | :--- | :--- | :--- |
| 1 | Design the system architecture diagram | ⏳ **Pending** | Needs to draw a formal visual diagram (e.g., Draw.io) for the report. |
| 2 | Select Architectural Pattern 1 | ✅ **Completed** | Selected Layered/MVC Architecture. |
| 3 | Implement Architectural Pattern 1 | ✅ **Completed** | Built the FastAPI shell, models, and command routes (`implementation_version_1`). |
| 4 | Document the implementation of Pattern 1 | ⏳ **Pending** | Needs to write the explanation for the report. |

### Person 4 – Software Architect & Developer
| Task | Description | Status | Notes |
| :--- | :--- | :--- | :--- |
| 1 | Select Architectural Pattern 2 | ✅ **Completed** | Selected CQRS for the ML integration. |
| 2 | Implement Architectural Pattern 2 | ✅ **Completed** | Built the Query side, trained the ML model, and built the analytics dashboard. |
| 3 | Integrate both implementations | ✅ **Completed** | Successfully linked the ML Engine to the FastAPI routers. |
| 4 | Fix bugs/issues reported during testing | ✅ **Completed** | Seeded the DB with actual dataset jobs to fix prediction errors. |
| 5 | Document the implementation of Pattern 2 | ✅ **Completed** | Finished via the `code_architecture.md` document. |
