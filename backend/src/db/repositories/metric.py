from typing import List, Optional

from src.db.models import Metric as ORMMetric
from src.db.repositories.base import BaseRepository
from src.entities import Metric, MetricCalculated


class MetricRepository(BaseRepository):
    def filter(self, sample_name: Optional[str] = None, version: Optional[str] = None) -> List[Metric]:
        query = self._session.query(ORMMetric)
        if version is not None:
            query = query.filter(ORMMetric.version == version)
        if sample_name is not None:
            query = query.filter(ORMMetric.sample.has(name=sample_name))

        return query.all()

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
