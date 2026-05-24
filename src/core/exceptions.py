import logging
from typing import Any, Optional

from fastapi import FastAPI, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.common.schemas import ErrorResponse

logger = logging.getLogger(__name__)


class AppException(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        code: Optional[str] = None,
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details

    def to_response(self) -> ErrorResponse:
        return ErrorResponse(message=self.message)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException) -> JSONResponse:
        logger.warning(
            "AppException [%s %s] code=%s status=%d message=%s",
            request.method,
            request.url.path,
            exc.code,
            exc.status_code,
            exc.message,
        )
        error_response = exc.to_response()
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump(),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            "Unexpected exception [%s %s]",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        error = ErrorResponse(message=str(exc))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error.model_dump(),
        )
