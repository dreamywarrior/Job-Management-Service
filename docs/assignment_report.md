# AIMLCZG546 - Assignment I Report Draft

## Group Details

Group No: `<Fill Group No>`

| Sl. No | BITS ID | Name | Contribution | Percentage |
|---|---|---|---|---|
| 1 | `<Fill>` | `<Fill>` | Requirements, implementation, documentation | `<Fill>` |
| 2 | `<Fill>` | `<Fill>` | `<Fill>` | `<Fill>` |
| 3 | `<Fill>` | `<Fill>` | `<Fill>` | `<Fill>` |
| 4 | `<Fill>` | `<Fill>` | `<Fill>` | `<Fill>` |

## 1. Domain and Problem Statement

The selected domain is online recruitment fraud detection. Job seekers increasingly rely on online job platforms, where fraudulent postings can collect sensitive personal information, demand money, or mislead applicants. The proposed system detects fake job postings from job details and description text, then presents a prediction, confidence score, risk level, and explanation.

## 2. Requirements Formulation Using GR4ML

The GR4ML views are documented separately:

- `gr4ml_business_view.md`
- `gr4ml_analytics_view.md`
- `gr4ml_data_preparation_view.md`

## 3. Top Quality Requirements

| Requirement | Justification |
|---|---|
| Explainability | Users must understand why a posting is risky before trusting the output. |
| Accuracy | False negatives expose applicants to fraud, while false positives affect legitimate recruiters. |
| Usability | Non-technical users should be able to enter or upload job postings easily. |

## 4. System Architecture

The architecture contains both ML and non-ML components:

- Streamlit UI
- Application controller
- Command bus and query bus
- Prediction microservice
- Reporting microservice
- Pipe-and-Filter prediction flow
- Text preprocessing
- Fake job classifier
- Explanation generator
- CSV data source
- Dashboard output

Architecture diagram source: `architecture_diagram.mmd`.

## 5. Architectural Patterns

### Pattern 1: CQRS Pattern

CQRS separates write-oriented actions from read-oriented queries. In this project, prediction requests are handled as commands through `CommandBus`, while dashboard summaries are handled as queries through `QueryBus`. This separation improves maintainability because prediction logic and reporting logic can evolve independently.

### Pattern 2: Microservices Pattern

The implementation separates responsibilities into service-style components. `PredictionService` owns ML inference, while `ReportingService` owns summaries used by the dashboard. In a production deployment, these components can be exposed as independent APIs.

### Pattern 3: Pipe-and-Filter Pattern

The prediction flow is implemented as a Pipe-and-Filter pattern:

Input -> preprocessing -> signal extraction -> risk scoring -> prediction -> explanation.

This pattern is suitable for ML systems because each stage can be tested and improved independently.

## 6. Implementation Summary

The implementation is a Streamlit application with three workflows:

- Single prediction
- Batch CSV analysis
- Architecture explanation

The app is located in `assignment_streamlit_app/streamlit_app.py`.

## 7. Screenshots

Add screenshots after running the application:

- Home/single prediction screen
- Batch analysis dashboard
- Architecture screen

## 8. Conclusion

The project demonstrates software engineering principles for an ML-based application by defining requirements, applying GR4ML views, designing architecture, implementing architectural patterns, and delivering a working Streamlit prototype.
