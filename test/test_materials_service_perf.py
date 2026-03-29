import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Set dummy env vars
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"

from app.modules.materials.schemas import MaterialSnippet
from app.service.materials import MaterialService


@pytest.mark.asyncio
async def test_save_snippets_uses_async_add_texts():
    # Mock dependencies
    with patch("app.service.materials.get_vector_store") as mock_get_vector_store, \
         patch("app.service.materials.AsyncSessionLocal") as mock_session_cls:

        # Setup mock vector store
        mock_vector_store = MagicMock()
        mock_vector_store.aadd_texts = AsyncMock()
        # Also mock add_texts to verify it's NOT called
        mock_vector_store.add_texts = MagicMock()

        mock_get_vector_store.return_value = mock_vector_store

        # Setup mock session
        mock_session = MagicMock() # Use MagicMock to avoid auto-async methods

        # Configure session to work as async context manager (if needed, but here it's the YIELDED object)
        # In code: async with AsyncSessionLocal() as session:
        # So AsyncSessionLocal() returns ctx, ctx.__aenter__ returns session.

        # Mock transaction (returned by session.begin())
        mock_transaction = MagicMock()
        mock_transaction.__aenter__ = AsyncMock(return_value=mock_session)
        mock_transaction.__aexit__ = AsyncMock(return_value=None)

        mock_session.begin.return_value = mock_transaction

        # session.add_all is synchronous
        mock_session.add_all = MagicMock()

        # Setup AsyncSessionLocal factory return value (the context manager)
        mock_session_ctx = MagicMock()
        mock_session_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_ctx.__aexit__ = AsyncMock(return_value=None)

        mock_session_cls.return_value = mock_session_ctx

        service = MaterialService()

        # Create dummy snippets with valid values
        snippets = [
            MaterialSnippet(
                category="动作",
                tags=["tag1"],
                mood="喜悦",
                essential_text="test content"
            )
        ]

        # Call save_snippets
        await service.save_snippets("Test Title", snippets)

        # Verify aadd_texts was called
        mock_vector_store.aadd_texts.assert_awaited_once()

        # Verify add_texts was NOT called
        mock_vector_store.add_texts.assert_not_called()

def test_get_vector_store_is_cached():
    # This test verifies that get_vector_store is cached
    from app.db.vector import get_vector_store

    # We patch the CLASSES, so we can count how many times they are instantiated
    with patch("app.db.vector.Chroma") as mock_chroma, \
         patch("app.db.vector.JinaEmbeddings"):

        # Clear cache if it exists (it doesn't yet in code, but we want to be safe)
        if hasattr(get_vector_store, "cache_clear"):
            get_vector_store.cache_clear()

        # First call
        get_vector_store()

        # Second call
        get_vector_store()

        # If cached, Chroma should be instantiated only once
        # Currently (before fix), it should be 2
        # After fix, it should be 1

        # We assert 1, expecting failure now
        assert mock_chroma.call_count == 1, f"Expected 1 call to Chroma, got {mock_chroma.call_count}"
