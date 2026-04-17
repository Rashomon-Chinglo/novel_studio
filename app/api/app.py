"""Application entrypoint for the API layer."""

from fastapi import FastAPI

from .errors import register_exception_handlers
from .routes.chapter import router as chapter_router
from .routes.materials import router as materials_router
from .routes.outline import router as outline_router


def create_app() -> FastAPI:
    app = FastAPI(title="Novel Studio API")
    register_exception_handlers(app)
    app.include_router(outline_router)
    app.include_router(materials_router)
    app.include_router(chapter_router)
    return app


app = create_app()
