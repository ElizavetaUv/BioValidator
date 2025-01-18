from typing import List

import pandas as pd

from src.db.interceptors import intercept_get_one_errors
from src.db.models import Mutation as ORMMutation
from src.db.models import Reference as ORMReference
from src.db.repositories.base import BaseRepository
from src.entities import Reference, ReferenceMetadata


class ReferenceRepository(BaseRepository):
    def create(self, name: str) -> None:
        orm_reference = ORMReference(name=name)
        self.session.add(orm_reference)
        self.session.commit()

    def get(self, name: str) -> Reference:
        with intercept_get_one_errors("Reference", name):
            orm_reference = self.session.query(ORMReference).where(ORMReference.name == name).one()

        return Reference.model_validate(orm_reference)

    def get_all(self) -> List[ReferenceMetadata]:
        orm_references = self.session.query(ORMReference).all()

        return [
            ReferenceMetadata(
                id=orm_ref.id,
                name=orm_ref.name,
            ) for orm_ref in orm_references
        ]

    def exists(self, name: str) -> bool:
        orm_sample = self.session.query(ORMReference).where(ORMReference.name == name).first()
        return orm_sample is not None

    def add_mutations(self, name: str, mutations_df: pd.DataFrame) -> None:
        reference = self.get(name)
        mutations = [
            ORMMutation(
                hugo_symbol=row["Hugo_Symbol"],
                variant_type=row["Variant_Type"],
                reference_allele=row["Reference_Allele"],
                chromosome=row["Chromosome"],
                start_position=row["Start_Position"],
                end_position=row["End_Position"],
                reference_id=reference.id,
            )
            for _, row in mutations_df.iterrows()
        ]
        self.session.bulk_save_objects(mutations)
        self.session.commit()
