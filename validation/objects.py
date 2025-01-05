from dataclasses import dataclass
from typing import List

import model

@dataclass
class Mutation:
    hugo_symbol: str
    variant_type: str
    reference_allele: str
    allele: str
    chromosome: int
    start_position: int
    end_position: int


@dataclass
class Reference:
    name: str
    mutations: List[Mutation]

@dataclass
class Sample:
    reference: Reference
    name: str
    

def converter(sample: model.Sample) -> Sample:
    reference = sample.reference
    mutations = reference.mutations
    ...
    return sample

