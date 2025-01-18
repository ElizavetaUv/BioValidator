
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel

from api.dependencies.services import get_reference_service
from src.entities import MolecularType, ReferenceMetadata
from src.services.reference import ReferenceService
from src.worker.helpers import Promise, TaskStatus

router = APIRouter(tags=["Reference"])


class CreateReferenceRequest(BaseModel):
    name: str



@router.post("/references", status_code=201, response_model=None)
def create_reference(
    reference_data: CreateReferenceRequest,
    reference_service: ReferenceService = Depends(get_reference_service),
) -> None:
    return reference_service.create(
        name=reference_data.name
    )

@router.get("/references", status_code=200, response_model=List[ReferenceMetadata])
def get_references(
    reference_service: ReferenceService = Depends(get_reference_service),
) -> List[ReferenceMetadata]:
    return reference_service.get_references()


@router.get("/references/{name}", status_code=200, response_model=ReferenceMetadata)
def get_reference(
    name: str,
    reference_service: ReferenceService = Depends(get_reference_service),
) -> ReferenceMetadata:
    return reference_service.get_reference(name)


@router.post("/references/{name}/calculate/mutations", status_code=200, response_model=Promise)
def calculate_reference_mutations(
    file: UploadFile,
    name: str,
    reference_service: ReferenceService = Depends(get_reference_service),
) -> Promise:
    return reference_service.calculate_mutations(
        molecular_type=MolecularType.GERMLINE,
        file_content=file.file,
        reference_name=name
    )


@router.get("/references/calculate/mutations/{task_id}/status", status_code=200, response_model=TaskStatus)
def calculate_reference_mutations(
    task_id: UUID,
    reference_service: ReferenceService = Depends(get_reference_service),
) -> TaskStatus:
    return reference_service.get_calculate_mutations_status(
        task_id=task_id
    )
