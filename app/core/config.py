from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Novel Studio"

    SQLITE_URL: str = f"sqlite+aiosqlite:///{DATA_DIR / 'novel.db'}"
    DATABASE_URL: str | None = None

    CHROMA_URL: str = f"{DATA_DIR / 'chroma_db'}"
    CHROMA_COLLECTION_NAME: str = "novel_snippets"

    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    # OPENAI_MODEL: str = "gemini-3-pro-preview"
    OPENAI_MODEL: str = "gemini-3-flash-preview"

    JINA_API_KEY: str
    JINA_API_URL: str = "https://api.jina.ai/v1/embeddings"

    @property
    def sqlalchemy_database_url(self) -> str:
        return self.DATABASE_URL or self.SQLITE_URL

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()  # type: ignore[missing-argument]
