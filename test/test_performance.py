import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Mock environment variables before importing anything from app
os.environ["JINA_API_KEY"] = "dummy"
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["CHROMA_URL"] = "dummy"
os.environ["CHROMA_COLLECTION_NAME"] = "dummy"
os.environ["JINA_API_URL"] = "dummy"
os.environ["SQLITE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.db.vector import get_vector_store
from app.service.materials import MaterialService


def test_get_vector_store_is_cached():
    # Clear cache to ensure clean state
    get_vector_store.cache_clear()

    with (
        patch("app.db.vector.JinaEmbeddings") as mock_embeddings,
        patch("app.db.vector.Chroma") as mock_chroma,
    ):
        v1 = get_vector_store()
        v2 = get_vector_store()

        assert v1 is v2
        assert mock_embeddings.call_count == 1
        assert mock_chroma.call_count == 1


@pytest.mark.asyncio
async def test_save_snippets_uses_async_add_texts():
    with (
        patch("app.service.materials.get_vector_store") as mock_get_vector_store,
        patch("app.service.materials.AsyncSessionLocal") as mock_session_cls,
    ):
        # Mock vector store
        mock_vector_store = MagicMock()
        mock_vector_store.aadd_texts = AsyncMock()
        mock_get_vector_store.return_value = mock_vector_store

        # Mock session
        # AsyncSessionLocal() -> context manager -> session
        mock_session = AsyncMock()
        mock_session_cls.return_value.__aenter__.return_value = mock_session

        # session.begin() -> context manager -> transaction
        # session.begin() is synchronous, returns an async context manager
        mock_session.begin = MagicMock()
        mock_transaction_cm = MagicMock()
        mock_transaction_cm.__aenter__ = AsyncMock()
        mock_transaction_cm.__aexit__ = AsyncMock()
        mock_session.begin.return_value = mock_transaction_cm

        # session.add_all is synchronous
        mock_session.add_all = MagicMock()

        service = MaterialService()

        # Create a mock snippet
        snippet = MagicMock()
        snippet.category = "test"
        snippet.tags = ["tag1"]
        snippet.mood = "happy"
        snippet.essential_text = "content"
        # model_dump_json returns a string
        snippet.model_dump_json.return_value = "{}"

        await service.save_snippets("Title", [snippet])

        # Verify aadd_texts is called and awaited
        mock_vector_store.aadd_texts.assert_awaited_once()
        # Verify add_all was called
        mock_session.add_all.assert_called_once()
