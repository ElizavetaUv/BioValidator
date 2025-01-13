from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field, conlist

from api.dependencies.services import get_metric_sample_service
from src.entities import Metric, MetricCompared
from src.services.metric_sample import MetricSampleService

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
    sample_name: Optional[str] = Query(default=None, alias="sampleName"),
    metric_sample_service: MetricSampleService = Depends(get_metric_sample_service),
) -> List[Metric]:
    return metric_sample_service.get_metrics(
        version=version,
        sample_name=sample_name,
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


@router.post("/metrics/calculate", status_code=200, response_model=None)
def calculate_metrics(
    body: ValidateSamplesRequest,
    metric_sample_service: MetricSampleService = Depends(get_metric_sample_service)
):
    metric_sample_service.validate(
        sample_names=body.sample_names,
        version=body.version,
    )
