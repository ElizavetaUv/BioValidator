
from typing import BinaryIO, List

from src.db.repositories.reference import ReferenceRepository
from src.entities import MolecularType, ReferenceMetadata
from src.errors import BioValidatorExternalError
from src.molecular.germline.prepare import parse_maf
from src.objstore.s3 import S3Store


class ReferenceService:
    def __init__(
        self,
        reference_repository: ReferenceRepository,
        object_store: S3Store,
    ) -> None:
        self._reference_repository = reference_repository
        self._object_store = object_store

    def create(
        self,
        name: str,
    ) -> None:
        if self._reference_repository.exists(name):
            raise BioValidatorExternalError(
                detail=f"Such reference with name: '{name}' already exists",
                status_code=409,
            )

        self._reference_repository.create(name)


    # TODO: run in worker
    def calculate_mutations(self, molecular_type: MolecularType, file_content: BinaryIO, reference_name: str) -> None:
        if molecular_type not in MolecularType.members():
            raise BioValidatorExternalError(
                detail=f"Such molecular type: '{molecular_type.name}' is not supported",
                status_code=400,
            )

        if not self._reference_repository.exists(reference_name):
            raise BioValidatorExternalError(
                detail=f"Such reference type: '{reference_name}' doesn't exist",
                status_code=404,
            )

        maf_df = parse_maf(file_content)

        self._reference_repository.add_mutations(
            name=reference_name,
            mutations_df=maf_df,
        )

    def get_reference(self, name: str) -> ReferenceMetadata:
        reference =  self._reference_repository.get(name)
        return ReferenceMetadata(
            id=reference.id,
            name=reference.name,
        )

    def get_references(self) -> List[ReferenceMetadata]:
        references = self._reference_repository.get_all()
        return references
