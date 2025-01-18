from typing import List, Optional

from src.db.models import Metric as ORMMetric
from src.db.models import Sample as ORMSample
from src.db.repositories.base import BaseRepository
from src.entities import Metric, MetricCalculated


class MetricRepository(BaseRepository):
    def filter(self, sample_names: Optional[List[str]] = None, version: Optional[str] = None) -> List[Metric]:
        query = self._session.query(ORMSample, ORMMetric).join(ORMMetric)
        if version is not None:
            query = query.filter(ORMMetric.version == version)
        if sample_names is not None:
            query = query.filter(ORMSample.name.in_(sample_names))

        metrics: List[Metric] = []
        response = query.all()

        for (sample, metric) in response:
            metrics.append(
                Metric(
                    id=metric.id,
                    name=metric.name,
                    version=metric.version,
                    value=metric.value,
                    sampleName=sample.name,
                )
            )

        return metrics

    def add_metrics(self, sample_id: int, metrics: List[MetricCalculated]) -> None:
        orm_metrics = [
            ORMMetric(
                sample_id=sample_id,
                **metric.model_dump(),
            )
            for metric in metrics
        ]
        self.session.bulk_save_objects(orm_metrics)
        self.session.commit()
