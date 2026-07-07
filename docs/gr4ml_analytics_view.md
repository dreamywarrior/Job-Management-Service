# GR4ML Analytics Design View

## ML Task

Binary classification of job postings:

- Fake
- Legitimate

## Inputs

- Job title
- Company name
- Location
- Employment type
- Salary range
- Job description

## Outputs

- Prediction label
- Confidence score
- Risk level
- Explanation signals

## Model Design

The prototype uses a transparent risk-scoring classifier inside a Pipe-and-Filter workflow to demonstrate the ML process. A production version can replace this layer with TF-IDF plus Logistic Regression, Random Forest, or transformer-based text classification.

## Evaluation Metrics

| Metric | Reason |
|---|---|
| Precision | Avoid marking legitimate jobs as fake |
| Recall | Catch as many fraudulent postings as possible |
| F1-score | Balance precision and recall |
| Latency | Keep interactive app response fast |

## Analytics Requirements

- The model shall generate predictions from text and structured job fields.
- The model shall provide an interpretable reason list.
- The batch workflow shall summarize prediction distribution.
- The architecture shall allow replacement of the classifier without rewriting the UI.
- Commands shall be separated from dashboard/reporting queries using CQRS.
- Prediction and reporting responsibilities shall be separated as microservice-style components.
