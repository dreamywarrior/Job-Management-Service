import re


def normalize_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def combine_job_fields(job: dict) -> str:
    fields = [
        job.get("title", ""),
        job.get("company", ""),
        job.get("location", ""),
        job.get("employment_type", ""),
        job.get("salary_range", ""),
        job.get("description", ""),
    ]
    return normalize_text(" ".join(str(field) for field in fields if field))
