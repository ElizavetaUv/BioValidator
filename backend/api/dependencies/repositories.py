from fastapi import Depends

from api.dependencies.share import Session, get_session
from src.db.repositories.metric import MetricRepository
from src.db.repositories.reference import ReferenceRepository
from src.db.repositories.sample import SampleRepository


def get_sample_repository(
    session: Session = Depends(get_session),
) -> SampleRepository:
    sample_repository = SampleRepository(session=session)
    return sample_repository


def get_reference_repository(
    session: Session = Depends(get_session),
) -> ReferenceRepository:
    reference_repository = ReferenceRepository(session=session)
    return reference_repository


def get_metric_repository(
    session: Session = Depends(get_session),
) -> MetricRepository:
    metric_repository = MetricRepository(session=session)
    return metric_repository
