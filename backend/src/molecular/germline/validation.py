
from typing import Hashable, List, Set, Tuple

import pandas as pd

from src.entities import MetricCalculated, MetricName, MutationCalculated, Sample
from src.molecular.base import ValidationInterface
from src.molecular.helpers import precision, recall


def extract_mutations_key(mutations: List[MutationCalculated]) -> Set[Tuple[Hashable]]:
    return {
        (
            str(mutation.chromosome),
            str(mutation.start_position),
            str(mutation.end_position),
            str(mutation.reference_allele),
        ) for mutation in mutations
    }


class GermlineValidation(ValidationInterface):
    def __init__(
        self,
        sample: Sample,
        version: str,
        input_maf: pd.DataFrame,
    ) -> None:
        self._sample = sample
        self._version = version
        self._input_maf = input_maf

    def validate(self) -> List[MetricCalculated]:

        calculated_mutations = [
            MutationCalculated(
                hugo_symbol=row["Hugo_Symbol"],
                variant_type=row["Variant_Type"],
                reference_allele=row["Reference_Allele"],
                chromosome=row["Chromosome"],
                start_position=row["Start_Position"],
                end_position=row["End_Position"],
            )
            for _, row in self._input_maf.iterrows()
        ]

        calculation_key = extract_mutations_key(calculated_mutations)
        reference_key = extract_mutations_key(self._sample.reference.mutations)

        true_positive = len(calculation_key.intersection(reference_key))
        false_positive = len(calculation_key.difference(reference_key))
        false_negative = len(reference_key.difference(calculation_key))

        calculated_precision = precision(true_positive, false_positive)
        calculated_recall = recall(true_positive, false_negative)


        return [
            MetricCalculated(
                name=MetricName.TP_GENES.value,
                version=self._version,
                value=str(true_positive),
            ),
            MetricCalculated(
                name=MetricName.FP_GENES.value,
                version=self._version,
                value=str(false_positive),
            ),
            MetricCalculated(
                name=MetricName.FN_GENES.value,
                version=self._version,
                value=str(false_negative),
            ),
            MetricCalculated(
                name=MetricName.PRECISION_GENE.value,
                version=self._version,
                value=str(calculated_precision),
            ),
            MetricCalculated(
                name=MetricName.RECALL_GENE.value,
                version=self._version,
                value=str(calculated_recall),
            ),
        ]
