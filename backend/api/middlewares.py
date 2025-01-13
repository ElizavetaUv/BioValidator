import logging

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from src.errors import BioValidatorExternalError


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except BioValidatorExternalError as err:
            return Response(
                err.detail,
                status_code=err.status_code,
            )
        except Exception as err:
            logging.exception(err)
            detail = f'Unexpected Error: {str(err)}'
            # TODO: Think about security
            return Response(
                detail,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
