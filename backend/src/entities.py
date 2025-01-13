from enum import Enum
from typing import List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field


class MetricName(Enum):
    PRECISION_GENE = "precision-gene"
    RECALL_GENE = "recall-gene"
    TP_GENES = "tp-genes"
    FP_GENES = "fp-genes"
    FN_GENES = "fn-genes"


class MolecularType(Enum):
    GERMLINE = "germline"

    @classmethod
    def members(cls) -> Set[str]:
        return {*cls.__members__.values()}


class MetricCalculated(BaseModel):
    name: str
    version: str
    value: str

class Metric(MetricCalculated):
    model_config = ConfigDict(from_attributes=True)

    id: int


class MutationCalculated(BaseModel):
    hugo_symbol: str
    variant_type: str
    reference_allele: str
    chromosome: Optional[int]
    start_position: Optional[int]
    end_position: Optional[int]

class Mutation(MutationCalculated):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ReferenceMetadata(BaseModel):
    id: int
    name: str

class Reference(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    mutations: List[Mutation]


class SampleMetadata(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    reference_name: str = Field(..., alias="referenceName")


class Sample(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    reference: Reference


class MetricCompared(BaseModel):
    name: MetricName
    sample_name: str = Field(..., alias="sampleName")
    current_version: str = Field(..., alias="currentVersion")
    compared_version: str = Field(..., alias="comparedVersion")
    current_value: str = Field(..., alias="currentValue")
    compared_value: str = Field(..., alias="comparedValue")
    diff_value: str = Field(..., alias="diffValue")
