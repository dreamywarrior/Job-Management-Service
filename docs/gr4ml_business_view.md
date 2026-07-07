# GR4ML Business View

## Business Goal

Reduce applicant exposure to fraudulent job postings by detecting suspicious jobs before users apply.

## Stakeholders

| Stakeholder | Goal | Concern |
|---|---|---|
| Job seeker | Avoid fraudulent postings | Clear and trustworthy prediction |
| Platform admin | Monitor risky listings | Scalable review workflow |
| Recruiter | Publish legitimate roles | Low false-positive rate |
| ML engineer | Maintain model quality | Data drift and explainability |

## Measurable Goals

| Goal | Metric | Target |
|---|---|---|
| Detect fake postings | Recall on fake class | >= 85% |
| Avoid blocking real jobs | Precision on fake class | >= 80% |
| Usable response time | Prediction latency | < 2 seconds |
| User understanding | Explanation coverage | At least 1 reason per prediction |

## Business Requirements

- The system shall accept a job posting as structured fields and free text.
- The system shall classify the posting as fake or legitimate.
- The system shall provide confidence and risk level.
- The system shall support batch review through CSV upload.
- The system shall provide dashboard summaries for decision support.
