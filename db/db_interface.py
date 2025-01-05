from sqlalchemy.orm import Session
from db.model import Sample, Reference, Mutation
from typing import List
import pandas as pd


def add_sample(session: Session, sample_name: str) -> Sample:
    sample = Sample(name=sample_name)
    session.add(sample)
    session.commit()
    return sample


def add_reference(session: Session, reference_name: str, sample_id: int) -> Reference:
    reference = Reference(name=reference_name, sample_id=sample_id)
    session.add(reference)
    session.commit()
    return reference


def add_mutations(session: Session, mutations_data: pd.DataFrame, reference_id: int) -> List[Mutation]:
    mutations = [
        Mutation(
            hugo_symbol=row["Hugo_Symbol"],
            variant_type=row["Variant_Type"],
            reference_allele=row["Reference_Allele"],
            chromosome=row["Chromosome"],
            start_position=row["Start_Position"],
            end_position=row["End_Position"],
            reference_id=reference_id,
        )
        for _, row in mutations_data.iterrows()
    ]
    session.add_all(mutations)
    session.commit()
    return mutations