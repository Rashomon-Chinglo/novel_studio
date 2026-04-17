"""HTTP error mapping for the API layer."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValueError)
    async def handle_value_error(_: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )
