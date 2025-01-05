from typing import List, Optional

from src.db.repositories.metric import MetricRepository
from src.db.repositories.sample import SampleRepository
from src.entities import Metric, MetricCompared, MolecularType
from src.errors import BioValidatorExternalError, BioValidatorInternalError
from src.molecular.germline.prepare import parse_maf
from src.molecular.germline.validation import GermlineValidation
from src.objstore.base import BaseStore
from src.objstore.samples import get_molecular_file_path


def try_float(v: any) -> Optional[float]:
    if v is None:
        return None
    try:
        return float(v)
    except ValueError:
        return None

def _strround(v: float, ndigits: int) -> str:
    return str(round(v, ndigits))

def get_diff(curval: Optional[str] = None, comval: Optional[str] = None, ndigits: int = 3, eps: float = 0.001) -> str:
    if curval is None and comval is None:
        raise BioValidatorInternalError(
            "There is an error with algorithm"
        )
    if curval is not None and comval is None:
        return f"{curval} (deleted)"

    if curval is None and comval is not None:
        return f"{comval} (added)"

    float_curval = try_float(curval)
    float_comval = try_float(comval)

    if float_curval is None or float_comval is None:
        if curval == comval:
            return f"{curval} (unchanged)"
        return f"{curval} ({comval})"

    diff = round(float_comval - float_curval, ndigits=ndigits)

    if abs(diff) < eps:
        return f"{curval} (unchanged)"

    res = _strround(abs(diff), ndigits=ndigits)
    sign = "+" if diff > 0 else "-"

    return f"{sign}{res}"


class Comparator:
    def __init__(
        self,
        sample_name: str,
        current_metrics: List[Metric],
        compared_metrics: List[Metric],
    ) -> None:
        self._sample_name = sample_name
        self._current_metrics = current_metrics
        self._compared_metrics = compared_metrics

    def compare(self) -> List[MetricCompared]:
        metric2current_metrics = {
            metric.name: metric for metric in self._current_metrics
        }

        metric2compared_metrics = {
            metric.name: metric for metric in self._compared_metrics
        }

        all_metric_names = set(metric2current_metrics.keys()).union(metric2compared_metrics.keys())

        metrics_compared = []
        for metric_name in sorted(all_metric_names):
            curmetric: Optional[Metric] = metric2current_metrics.get(metric_name, None)
            commetric: Optional[Metric] = metric2compared_metrics.get(metric_name, None)

            current_version = curmetric.version if curmetric is not None else "(void)"
            compared_version = commetric.version if commetric is not None else "(void)"

            current_value = curmetric.value if curmetric is not None else "(void)"
            compared_value = commetric.value if commetric is not None else "(void)"

            diff = get_diff(
                curmetric.value if curmetric is not None else None,
                commetric.value if commetric is not None else None,
            )

            metrics_compared.append(
                MetricCompared(
                    name=metric_name,
                    sampleName=self._sample_name,
                    currentVersion=current_version,
                    comparedVersion=compared_version,
                    currentValue=current_value,
                    comparedValue=compared_value,
                    diffValue=diff
                )
            )
        return metrics_compared

class MetricSampleService:
    def __init__(
        self,
        sample_repository: SampleRepository,
        metric_repository: MetricRepository,
        object_store: BaseStore,
    ) -> None:
        self._sample_repository = sample_repository
        self._metric_repository = metric_repository
        self._object_store = object_store

    def compare(
        self,
        current_version: str,
        compared_version: str,
        sample_names: List[str]
    ) -> List[MetricCompared]:
        metrics_compared: List[MetricCompared] = []

        for sample_name in sample_names:
            if not self._sample_repository.exists(sample_name):
                raise BioValidatorExternalError(
                    detail=f"Such sample type: '{sample_name}' doesn't exist",
                    status_code=404,
                )

        for sample_name in sample_names:
            current_metrics = self._metric_repository.filter(sample_name=sample_name, version=current_version)
            compared_metrics = self._metric_repository.filter(sample_name=sample_name, version=compared_version)

            comparator = Comparator(
                sample_name=sample_name,
                current_metrics=current_metrics,
                compared_metrics=compared_metrics,
            )

            mc = comparator.compare()
            metrics_compared.extend(mc)

        return metrics_compared

    def validate(self, sample_names: List[str], version: str) -> None:
        for sample_name in sample_names:
            if not self._sample_repository.exists(sample_name):
                raise BioValidatorExternalError(
                    detail=f"Such sample type: '{sample_name}' doesn't exist",
                    status_code=404,
                )
            sample = self._sample_repository.get(name=sample_name)
            if len(sample.reference.mutations) == 0:
                raise BioValidatorExternalError(
                    detail=f"Reference: '{sample.reference.name}' has no calculated mutations",
                    status_code=400,
                )

            molecular_file_path = get_molecular_file_path(sample_name, MolecularType.GERMLINE)

            if not self._object_store.object_exists(molecular_file_path):
                raise BioValidatorExternalError(
                    detail=f"Sample: '{sample_name}' has no mutations",
                    status_code=404,
                )
            raw_maf = self._object_store.download_object(molecular_file_path)
            maf_df = parse_maf(raw_maf)
            del raw_maf

            validator = GermlineValidation(sample, version, maf_df)
            metrics = validator.validate()
            self._metric_repository.add_metrics(
                sample_id=sample.id,
                metrics=metrics,
            )

    def get_metrics(self, sample_name: Optional[str] = None, version: Optional[str] = None) -> List[Metric]:
        return self._metric_repository.filter(sample_name=sample_name, version=version)
