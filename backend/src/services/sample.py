from typing import BinaryIO, List

from src.db.repositories.reference import ReferenceRepository
from src.db.repositories.sample import SampleRepository
from src.entities import MolecularType, Sample, SampleMetadata
from src.errors import BioValidatorExternalError
from src.objstore.s3 import S3Store
from src.objstore.samples import get_molecular_file_path


class SampleService:
    def __init__(
        self,
        sample_repository: SampleRepository,
        reference_repository: ReferenceRepository,
        object_store: S3Store,
    ) -> None:
        self._sample_repository = sample_repository
        self._reference_repository = reference_repository
        self._object_store = object_store

    def create(
        self,
        sample_name: str,
        reference_name: str
    ) -> None:
        if self._sample_repository.exists(sample_name):
            raise BioValidatorExternalError(
                detail=f"Such sample type: '{sample_name}' already exists",
                status_code=409,
            )
        if not self._reference_repository.exists(reference_name):
            raise BioValidatorExternalError(
                detail=f"Such reference type: '{reference_name}' doesn't exist",
                status_code=404,
            )

        reference = self._reference_repository.get(reference_name)
        self._sample_repository.create(
            sample_name,
            reference.id
        )


    def upload_file(self, molecular_type: MolecularType, file_content: BinaryIO, sample_name: str) -> None:
        if molecular_type not in MolecularType.members():
            raise BioValidatorExternalError(
                detail=f"Such molecular type: '{molecular_type.value}' is not supported",
                status_code=400,
            )

        if not self._sample_repository.exists(sample_name):
            raise BioValidatorExternalError(
                detail=f"Such sample: '{sample_name}' doesn't exist",
                status_code=404
            )
        # TODO: Add maf validation
        self._object_store.upload_object(
            content=file_content,
            path=get_molecular_file_path(
                sample_name,
                molecular_type
            )
        )


    def get_sample(self, name: str) -> Sample:
        sample =  self._sample_repository.get(name)
        return sample

    def get_samples(self) -> List[SampleMetadata]:
        samples =  self._sample_repository.get_all()
        return samples
