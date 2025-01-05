from contextlib import contextmanager
from typing import Generator

from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from src.errors import BioValidatorExternalError


@contextmanager
def intercept_get_one_errors(entity_name: str, value: any) -> Generator[None, None, None]:
    try:
        yield
    except NoResultFound as exc:
        raise BioValidatorExternalError(
            detail=f"Such {entity_name} with value: '{str(value)}' doesn't exist",
            status_code=404,
        ) from exc
    except MultipleResultsFound:
        raise BioValidatorExternalError(
            detail=f"Multiple values: {value} found for {entity_name}",
            status_code=409,
        )
    except Exception as exc:
        raise exc
