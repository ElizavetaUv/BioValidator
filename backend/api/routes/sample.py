from typing import List

from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel, Field

from api.dependencies.services import get_sample_service
from src.entities import MolecularType, Sample, SampleMetadata
from src.services.sample import SampleService

router = APIRouter(tags=["Sample"])


class CreateSampleRequest(BaseModel):
    name: str
    reference_name: str = Field(..., alias="referenceName")


# class ValidateSamplesRequest(BaseModel):
#     sample_names: conlist(str, min_length=1) = Field(..., "sampleNames")
#     version: str


@router.post("/samples", status_code=201, response_model=None)
def create_sample(
    sample_data: CreateSampleRequest,
    sample_service: SampleService = Depends(get_sample_service),
) -> None:
    return sample_service.create(
        sample_name=sample_data.name,
        reference_name=sample_data.reference_name,
    )

@router.get("/samples", status_code=200, response_model=List[SampleMetadata])
def get_samples(
    sample_service: SampleService = Depends(get_sample_service),
):
    return sample_service.get_samples()


@router.get("/samples/{name}", status_code=200, response_model=Sample)
def get_sample(
    name: str,
    sample_service: SampleService = Depends(get_sample_service)
) -> Sample:
    return sample_service.get_sample(name)


# @router.post("/samples/validate", status_code=200, response_model=None)
# def validate_sample(
#     body: ValidateSamplesRequest,
#     sample_service: SampleService = Depends(get_sample_service)
# ):
#     ...
    # return sample_service.get_sample(name)

@router.get("/samples/{name}/metrics", status_code=200, response_model=SampleMetadata)
def get_sample_metrics(
    name: str,
    sample_service: SampleService = Depends(get_sample_service)
):
    # return sample_service.get(name)
    ...


@router.post("/samples/{name}/molecular/mutations", status_code=200, response_model=None)
def post_molecular_data(
    file: UploadFile,
    name: str,
    sample_service: SampleService = Depends(get_sample_service),
) -> None:
    sample_service.upload_file(
        molecular_type=MolecularType.GERMLINE,
        file_content=file.file,
        sample_name=name,
    )
