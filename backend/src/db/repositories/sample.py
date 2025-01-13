from typing import List, Optional

from src.db.interceptors import intercept_get_one_errors
from src.db.models import Metric as ORMMetric
from src.db.models import Sample as ORMSample
from src.db.repositories.base import BaseRepository
from src.entities import Metric, MetricCalculated, Sample, SampleMetadata


class SampleRepository(BaseRepository):
    def create(self, name: str, reference_id: int) -> None:
        orm_sample = ORMSample(name=name, reference_id=reference_id)
        self.session.add(orm_sample)
        self.session.commit()

    def get(self, name: str) -> Sample:
        with intercept_get_one_errors("Sample", name):
            orm_sample = self.session.query(ORMSample).where(ORMSample.name == name).one()

        return Sample.model_validate(orm_sample)

    def exists(self, name: str) -> bool:
        orm_sample = self.session.query(ORMSample).where(ORMSample.name == name).first()
        return orm_sample is not None

    # TODO: Without references
    def get_all(self) -> List[SampleMetadata]:
        return [
            SampleMetadata(
                id=sample.id,
                name=sample.name,
                referenceName=sample.reference.name,
            )
            for sample in self.session.query(ORMSample).all()
        ]

    def get_metrics(self, name: Optional[str] = None, version: Optional[str] = None) -> List[Metric]:
        with intercept_get_one_errors("Sample", name):
            orm_sample = self.session.query(ORMSample).where(ORMSample.name == name).one()

        metrics = [
            Metric.validate_model(orm_metric) for orm_metric in orm_sample.metrics
        ]
        return metrics

    def add_metrics(self, sample_id: int, metrics: List[MetricCalculated]) -> None:
        orm_metrics = [
            ORMMetric(
                sample_id=sample_id,
                **metric.model_dump(),
            )
            for metric in metrics
        ]
        self.session.add_all(orm_metrics)
        self.session.commit()
