# main.py (or wherever you define your FastAPI app)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mcp_notebooks.core.exceptions import KernelCreationError, SessionNotFoundError


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(KernelCreationError)
    async def kernel_creation_exception_handler(
        request: Request, exc: KernelCreationError
    ):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc), "error": "KernelCreationError"},
        )

    @app.exception_handler(SessionNotFoundError)
    async def session_not_found_exception_handler(
        request: Request, exc: SessionNotFoundError
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc), "error": "SessionNotFoundError"},
        )
