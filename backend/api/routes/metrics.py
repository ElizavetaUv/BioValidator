from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field, conlist

from api.dependencies.services import get_metric_sample_service
from src.entities import Metric, MetricCompared
from src.services.metric_sample import MetricSampleService
from src.worker.helpers import Promise, TaskStatus

router = APIRouter(tags=["Metric"])

class ValidateSamplesRequest(BaseModel):
    sample_names: conlist(str, min_length=1) = Field(..., alias="sampleNames")
    version: str


class CompareMetrics(BaseModel):
    sample_names: conlist(str, min_length=1) = Field(..., alias="sampleNames")
    current_version: str = Field(..., alias="currentVersion")
    compared_version: str = Field(..., alias="comparedVersion")


@router.get("/metrics", status_code=200, response_model=List[Metric])
def get_metrics(
    version: Optional[str] = Query(default=None),
    sample_names: Optional[List[str]] = Query(default=None, alias="sampleName"),
    metric_sample_service: MetricSampleService = Depends(get_metric_sample_service),
) -> List[Metric]:
    return metric_sample_service.get_metrics(
        version=version,
        sample_names=sample_names,
    )


@router.post("/metrics/compare", status_code=200, response_model=List[MetricCompared])
def compare_versions(
    body: CompareMetrics,
    metric_sample_service: MetricSampleService = Depends(get_metric_sample_service)
) -> List[MetricCompared]:
    return metric_sample_service.compare(
        current_version=body.current_version,
        compared_version=body.compared_version,
        sample_names=body.sample_names,
    )


@router.post("/metrics/calculate", status_code=200, response_model=Promise)
def calculate_metrics(
    body: ValidateSamplesRequest,
    metric_sample_service: MetricSampleService = Depends(get_metric_sample_service)
) -> Promise:
    return metric_sample_service.validate(
        sample_names=body.sample_names,
        version=body.version,
    )


@router.get("/metrics/{task_id}/calculate/status", status_code=200, response_model=TaskStatus)
def calculate_metrics(
    task_id: UUID,
    metric_sample_service: MetricSampleService = Depends(get_metric_sample_service)
):
    return metric_sample_service.get_validate_status(
        task_id=task_id
    )
