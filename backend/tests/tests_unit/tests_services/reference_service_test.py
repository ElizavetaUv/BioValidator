import pytest

from src.db.repositories.reference import ReferenceRepository
from src.errors import BioValidatorExternalError
from src.services.reference import ReferenceService


def test_create_reference(mock_session, mock_object_store) -> None:
    reference_repo = ReferenceRepository(
        session=mock_session
    )
    reference_service = ReferenceService(
        reference_repository=reference_repo,
        object_store=mock_object_store,
    )
    reference_service.create("sam-test")
    ref = reference_service.get_reference("sam-test")

    assert ref.name == "sam-test"
    assert ref.id == 1


def test_create_reference_several_times(mock_session, mock_object_store) -> None:
    reference_repo = ReferenceRepository(
        session=mock_session
    )
    reference_service = ReferenceService(
        reference_repository=reference_repo,
        object_store=mock_object_store,
    )
    reference_service.create("sam-test")
    with pytest.raises(BioValidatorExternalError, match="Such reference with name: 'sam-test' already exists"):
        reference_service.create("sam-test")



def test_get_empty_references(mock_session, mock_object_store) -> None:
    reference_repo = ReferenceRepository(
        session=mock_session
    )
    reference_service = ReferenceService(
        reference_repository=reference_repo,
        object_store=mock_object_store,
    )
    refs = reference_service.get_references()

    assert len(refs) == 0


def test_get_unexist_reference(mock_session, mock_object_store) -> None:
    reference_repo = ReferenceRepository(
        session=mock_session
    )
    reference_service = ReferenceService(
        reference_repository=reference_repo,
        object_store=mock_object_store,
    )
    with pytest.raises(BioValidatorExternalError, match="Such Reference with value: 'sam-test' doesn't exist"):
        reference_service.get_reference("sam-test")


def test_get_references_with_exist_entities(mock_session, mock_object_store) -> None:
    reference_repo = ReferenceRepository(
        session=mock_session
    )
    reference_service = ReferenceService(
        reference_repository=reference_repo,
        object_store=mock_object_store,
    )
    reference_service.create("sam-test")
    reference_service.create("sam-test2")

    refs = reference_service.get_references()

    assert len(refs) == 2


