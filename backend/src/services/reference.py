
from typing import BinaryIO, List
from uuid import UUID

import src.worker.tasks as tasks
from src.db.repositories.reference import ReferenceRepository
from src.entities import MolecularType, ReferenceMetadata
from src.errors import BioValidatorExternalError
from src.objstore.paths import get_reference_molecular_file_path
from src.objstore.s3 import S3Store
from src.worker.helpers import Promise, TaskStatus, get_result


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

    def calculate_mutations(self, molecular_type: MolecularType, file_content: BinaryIO, reference_name: str) -> Promise:
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
        reference_molecular_path = get_reference_molecular_file_path(
            reference_name=reference_name,
            molecular_type=molecular_type
        )
        self._object_store.upload_object(
            file_content,
            path=reference_molecular_path
        )

        task = tasks.calculate_reference.send(reference_name=reference_name, molecular_type=molecular_type.value)
        return Promise(
            promiseId=task.message_id
        )

    def get_calculate_mutations_status(self, task_id: UUID) -> TaskStatus:
        return get_result(tasks.calculate_reference, task_id)

    def get_reference(self, name: str) -> ReferenceMetadata:
        reference =  self._reference_repository.get(name)
        return ReferenceMetadata(
            id=reference.id,
            name=reference.name,
        )

    def get_references(self) -> List[ReferenceMetadata]:
        references = self._reference_repository.get_all()
        return references
