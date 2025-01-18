from enum import Enum
from typing import Callable, Optional
from uuid import UUID

from dramatiq.results import ResultFailure, ResultMissing
from pydantic import BaseModel, Field

from src.errors import BioValidatorExternalError


class Statuses(Enum):
    PROGRESS = "PROGRESS"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    UNKNOWN = "UNKNOWN"


class TaskStatus(BaseModel):
    status: Statuses
    details: Optional[str] = None


class Promise(BaseModel):
    promise_id: UUID = Field(..., alias="promiseId")


def get_result(task: Callable, task_id: UUID) -> TaskStatus:
    message = task.message().copy(message_id=task_id)
    status = Statuses.UNKNOWN
    details = "<Unknown>"
    try:
        message.get_result()
        status = Statuses.COMPLETED
        details = None
    except ResultMissing:
        status = Statuses.PROGRESS
        details = None
    except ResultFailure as exc:
        status = Statuses.FAILED

        details = "Unexpected error. Please contact maintainers"
        if exc.orig_exc_type == BioValidatorExternalError.__name__:
            details = str(exc.orig_exc_msg)

    return TaskStatus(
        status=status,
        details=details
    )
