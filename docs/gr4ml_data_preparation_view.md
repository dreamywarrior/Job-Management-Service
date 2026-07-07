# GR4ML Data Preparation View

## Data Sources

- User-entered job postings.
- Uploaded CSV files.
- Sample job posting CSV included in the project.

## Data Schema

| Field | Type | Description |
|---|---|---|
| title | Text | Job role title |
| company | Text | Hiring company |
| location | Text | Job location |
| employment_type | Category | Full-time, contract, part-time, temporary |
| salary_range | Text | Advertised compensation |
| description | Text | Main job posting content |

## Preparation Steps

1. Merge structured and free-text fields.
2. Remove HTML tags.
3. Normalize whitespace.
4. Convert text to lowercase.
5. Detect suspicious terms and trust signals.
6. Generate model-ready risk score.

## Data Quality Requirements

- Missing optional fields should not break prediction.
- CSV uploads must contain the expected columns.
- Text normalization must preserve meaningful terms such as salary, remote work, and payment instructions.
