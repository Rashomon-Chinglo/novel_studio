from pathlib import Path
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Novel Studio"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8976
    API_RELOAD: bool = True
    API_INIT_PERSISTENCE_ON_STARTUP: bool = True
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    SQLITE_URL: str = f"sqlite+aiosqlite:///{DATA_DIR / 'novel.db'}"
    DATABASE_URL: str | None = None

    CHROMA_URL: str = f"{DATA_DIR / 'chroma_db'}"
    CHROMA_COLLECTION_NAME: str = "novel_snippets"

    OPENAI_API_KEY: str | None = None
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gemini-3-flash-preview"

    JINA_API_KEY: str | None = None
    JINA_API_URL: str = "https://api.jina.ai/v1/embeddings"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> Any:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @property
    def sqlalchemy_database_url(self) -> str:
        return self.DATABASE_URL or self.SQLITE_URL

    def require_openai_api_key(self) -> str:
        if not self.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is required for LLM operations.")
        return self.OPENAI_API_KEY

    def require_jina_api_key(self) -> str:
        if not self.JINA_API_KEY:
            raise RuntimeError("JINA_API_KEY is required for vector search operations.")
        return self.JINA_API_KEY

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
