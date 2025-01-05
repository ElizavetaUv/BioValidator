from fastapi import Depends

from api.dependencies.repositories import get_metric_repository, get_reference_repository, get_sample_repository
from api.dependencies.share import S3Store, get_object_store
from src.db.repositories.metric import MetricRepository
from src.db.repositories.reference import ReferenceRepository
from src.db.repositories.sample import SampleRepository
from src.services.metric_sample import MetricSampleService
from src.services.reference import ReferenceService
from src.services.sample import SampleService

__all__ = [
    "get_sample_service",
    "get_reference_service",
    "get_metric_sample_service",
]

def get_sample_service(
    sample_repository: SampleRepository = Depends(get_sample_repository),
    reference_repository: ReferenceRepository = Depends(get_reference_repository),
    object_store: S3Store = Depends(get_object_store),
) -> SampleService:
    sample_service = SampleService(
        sample_repository=sample_repository,
        reference_repository=reference_repository,
        object_store=object_store
    )
    return sample_service


def get_reference_service(
    reference_repository: ReferenceRepository = Depends(get_reference_repository),
    object_store: S3Store = Depends(get_object_store),
) -> ReferenceService:
    reference_service = ReferenceService(
        reference_repository=reference_repository,
        object_store=object_store
    )
    return reference_service


def get_metric_sample_service(
    sample_repository: SampleRepository = Depends(get_sample_repository),
    metric_repository: MetricRepository = Depends(get_metric_repository),
    object_store: S3Store = Depends(get_object_store),
) -> MetricSampleService:
    reference_service = MetricSampleService(
        sample_repository=sample_repository,
        metric_repository=metric_repository,
        object_store=object_store,
    )
    return reference_service
