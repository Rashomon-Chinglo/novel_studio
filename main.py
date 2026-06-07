import uvicorn

from app.core.config import settings


def main() -> None:
    uvicorn.run(
        "app.api.app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
    )


if __name__ == "__main__":
    main()
