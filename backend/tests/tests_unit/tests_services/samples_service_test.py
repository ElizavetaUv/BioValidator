import pytest

from src.db.repositories.reference import ReferenceRepository
from src.db.repositories.sample import SampleRepository
from src.errors import BioValidatorExternalError
from src.services.reference import ReferenceService
from src.services.sample import SampleService


@pytest.fixture
def create_mock_reference_1(mock_session, mock_object_store):
    reference_repo = ReferenceRepository(
        session=mock_session
    )
    reference_service = ReferenceService(
        reference_repository=reference_repo,
        object_store=mock_object_store,
    )

    reference_service.create("test-ref")
    return reference_service.get_reference("test-ref")


def test_create_sample(mock_session, mock_object_store, create_mock_reference_1) -> None:
    reference_repo = ReferenceRepository(
        session=mock_session
    )
    sample_repo = SampleRepository(
        session=mock_session
    )
    sample_service = SampleService(
        sample_repository=sample_repo,
        reference_repository=reference_repo,
        object_store=mock_object_store,
    )
    sample_service.create("sam-test", reference_name="test-ref")
    ref = sample_service.get_sample("sam-test")

    assert ref.name == "sam-test"
    assert ref.id == 1


def test_create_sample_with_unexist_reference(mock_session, mock_object_store, create_mock_reference_1) -> None:
    reference_repo = ReferenceRepository(
        session=mock_session
    )
    sample_repo = SampleRepository(
        session=mock_session
    )
    sample_service = SampleService(
        sample_repository=sample_repo,
        reference_repository=reference_repo,
        object_store=mock_object_store,
    )
    with pytest.raises(BioValidatorExternalError, match="Such reference type: 'unexist' doesn't exist"):
        sample_service.create("sam-test", reference_name="unexist")



def test_create_sample_several_times(mock_session, mock_object_store, create_mock_reference_1) -> None:
    reference_repo = ReferenceRepository(
        session=mock_session
    )
    sample_repo = SampleRepository(
        session=mock_session
    )
    sample_service = SampleService(
        sample_repository=sample_repo,
        reference_repository=reference_repo,
        object_store=mock_object_store,
    )
    sample_service.create("sam-test", reference_name="test-ref")
    with pytest.raises(BioValidatorExternalError, match="Such sample type: 'sam-test' already exists"):
        sample_service.create("sam-test", reference_name="test-ref")



def test_get_empty_sample(mock_session, mock_object_store) -> None:
    reference_repo = ReferenceRepository(
        session=mock_session
    )
    sample_repo = SampleRepository(
        session=mock_session
    )
    sample_service = SampleService(
        sample_repository=sample_repo,
        reference_repository=reference_repo,
        object_store=mock_object_store,
    )
    refs = sample_service.get_samples()

    assert len(refs) == 0


def test_get_unexist_sample(mock_session, mock_object_store) -> None:
    reference_repo = ReferenceRepository(
        session=mock_session
    )
    sample_repo = SampleRepository(
        session=mock_session
    )
    sample_service = SampleService(
        sample_repository=sample_repo,
        reference_repository=reference_repo,
        object_store=mock_object_store,
    )
    with pytest.raises(BioValidatorExternalError, match="Such Sample with value: 'sam-test' doesn't exist"):
        sample_service.get_sample("sam-test")


def test_get_references_with_exist_entities(mock_session, mock_object_store, create_mock_reference_1) -> None:
    reference_repo = ReferenceRepository(
        session=mock_session
    )
    sample_repo = SampleRepository(
        session=mock_session
    )
    sample_service = SampleService(
        sample_repository=sample_repo,
        reference_repository=reference_repo,
        object_store=mock_object_store,
    )
    sample_service.create("sam-test", "test-ref")
    sample_service.create("sam-test2", "test-ref")
    sample_service.create("sam-test3", "test-ref")

    sampls = sample_service.get_samples()

    assert len(sampls) == 3


