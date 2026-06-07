"""Application entrypoint for the API layer."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from app.core.config import settings
from app.persistence import initialize_persistence

from .errors import register_exception_handlers
from .routes.chapter import router as chapter_router
from .routes.materials import router as materials_router
from .routes.outline import router as outline_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    if settings.API_INIT_PERSISTENCE_ON_STARTUP:
        await initialize_persistence(initialize_vector_store=False)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=f"{settings.PROJECT_NAME} API",
        lifespan=lifespan,
        middleware=[
            Middleware(
                CORSMiddleware,  # type: ignore[invalid-argument-type]
                allow_origins=settings.BACKEND_CORS_ORIGINS,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ],
    )

    register_exception_handlers(app)

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(outline_router)
    app.include_router(materials_router)
    app.include_router(chapter_router)
    return app


app = create_app()
