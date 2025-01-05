
from typing import List

from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel

from api.dependencies.services import get_reference_service
from src.entities import MolecularType, Reference, ReferenceMetadata
from src.services.reference import ReferenceService

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


# TODO: Return promise id?
@router.post("/references/{name}/calculate/mutations", status_code=200, response_model=None)
def calculate_reference(
    file: UploadFile,
    name: str,
    reference_service: ReferenceService = Depends(get_reference_service),
) -> Reference:
    reference_service.calculate_mutations(
        molecular_type=MolecularType.GERMLINE,
        file_content=file.file,
        reference_name=name
    )
