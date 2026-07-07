from dataclasses import dataclass
from typing import Callable


@dataclass
class PredictJobCommand:
    job: dict


@dataclass
class BatchPredictionQuery:
    jobs: list[dict]


class PipeAndFilter:
    def __init__(self, filters: list[Callable[[dict], dict]]):
        self.filters = filters

    def run(self, payload: dict) -> dict:
        for filter_step in self.filters:
            payload = filter_step(payload)
        return payload


class PredictionService:
    def __init__(self, predictor: Callable[[dict], dict]):
        self.predictor = predictor

    def predict(self, command: PredictJobCommand) -> dict:
        pipe = PipeAndFilter(
            [
                lambda payload: {"job": payload["job"], "result": self.predictor(payload["job"])},
                lambda payload: {**payload["job"], **payload["result"]},
            ]
        )
        return pipe.run({"job": command.job})


class ReportingService:
    def summarize(self, query: BatchPredictionQuery) -> dict:
        total = len(query.jobs)
        fake = sum(1 for job in query.jobs if job.get("prediction") == "Fake")
        legitimate = sum(1 for job in query.jobs if job.get("prediction") == "Legitimate")
        return {
            "total": total,
            "fake": fake,
            "legitimate": legitimate,
        }


class CommandBus:
    def __init__(self, prediction_service: PredictionService):
        self.prediction_service = prediction_service

    def execute(self, command: PredictJobCommand) -> dict:
        return self.prediction_service.predict(command)


class QueryBus:
    def __init__(self, reporting_service: ReportingService):
        self.reporting_service = reporting_service

    def execute(self, query: BatchPredictionQuery) -> dict:
        return self.reporting_service.summarize(query)
