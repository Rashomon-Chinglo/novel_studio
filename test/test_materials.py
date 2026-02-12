import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Set environment variables BEFORE importing app modules to avoid validation errors
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"

from app.modules.materials.schemas import MaterialSnippet
from app.service.materials import MaterialService


@pytest.mark.asyncio
async def test_save_snippets_uses_async_add_texts():
    with (
        patch("app.service.materials.get_vector_store") as mock_get_vector_store,
        patch("app.service.materials.AsyncSessionLocal") as mock_session_local,
        patch("app.service.materials.MaterialEngine"),
    ):
        # Setup vector store mock
        mock_vector_store = MagicMock()
        mock_vector_store.aadd_texts = AsyncMock()
        mock_vector_store.add_texts = MagicMock()  # Mock the sync one too
        mock_get_vector_store.return_value = mock_vector_store

        # Setup session mock
        # AsyncSessionLocal() returns a session (AsyncMock usually works for the session itself if used as async context manager)
        mock_session = AsyncMock()
        mock_session_local.return_value = mock_session
        # When entering context manager
        mock_session.__aenter__.return_value = mock_session

        # session.begin() is synchronous but returns an async context manager
        mock_transaction = MagicMock()
        mock_transaction.__aenter__ = AsyncMock(return_value=mock_transaction)
        mock_transaction.__aexit__ = AsyncMock(return_value=None)

        # IMPORTANT: session.begin is a property/method on the session instance
        mock_session.begin = MagicMock(return_value=mock_transaction)

        # Initialize service
        service = MaterialService()
        assert service.vector_store == mock_vector_store

        # Test data
        snippets = [
            MaterialSnippet(
                category="对话", tags=["tag1", "tag2"], mood="喜悦", essential_text="test_content"
            )
        ]

        # Run method
        await service.save_snippets("Test Title", snippets)

        # Verify aadd_texts was called
        # This assertion is expected to FAIL before the fix
        mock_vector_store.aadd_texts.assert_awaited_once()

        # Verify add_texts was NOT called
        mock_vector_store.add_texts.assert_not_called()
