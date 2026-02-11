import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Set dummy env vars for Settings validation
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"

# Import after setting env vars
try:
    from app.db.vector import get_vector_store
    from app.modules.materials.schemas import MaterialSnippet
    from app.service.materials import MaterialService
except ImportError:
    pass


@pytest.mark.asyncio
async def test_save_snippets_async():
    """Verify that save_snippets uses async add_texts."""
    # Mock get_vector_store to return a mock vector store
    with patch("app.service.materials.get_vector_store") as mock_get_vs:
        mock_vector_store = MagicMock()
        mock_vector_store.aadd_texts = AsyncMock()
        mock_vector_store.add_texts = MagicMock()
        mock_get_vs.return_value = mock_vector_store

        # Mock AsyncSessionLocal
        with patch("app.service.materials.AsyncSessionLocal") as mock_session_local:
            # The factory returns an object that can be used in 'async with'
            mock_db_session = MagicMock()
            mock_session_local.return_value = mock_db_session

            # When entering the session context, we get the session object
            mock_session_obj = MagicMock()
            mock_db_session.__aenter__.return_value = mock_session_obj

            # session.begin() returns a context manager, NOT a coroutine
            mock_transaction_ctx = MagicMock()
            mock_session_obj.begin.return_value = mock_transaction_ctx
            # Entering transaction context
            mock_transaction_ctx.__aenter__.return_value = MagicMock()

            # Mock MaterialEngine to prevent instantiation issues if any
            with patch("app.service.materials.MaterialEngine"):
                service = MaterialService()

                snippets = [
                    MaterialSnippet(
                        category="对话", tags=["tag1"], mood="喜悦", essential_text="content"
                    )
                ]

                await service.save_snippets("Test Title", snippets)

                # Check if aadd_texts was called
                if mock_vector_store.aadd_texts.called:
                    print("SUCCESS: aadd_texts was called")
                else:
                    print("FAILURE: aadd_texts was NOT called")

                if mock_vector_store.add_texts.called:
                    print("FAILURE: add_texts (sync) was called")
                else:
                    print("SUCCESS: add_texts (sync) was NOT called")

                assert mock_vector_store.aadd_texts.called, "Should call async aadd_texts"
                assert not mock_vector_store.add_texts.called, "Should NOT call sync add_texts"


def test_get_vector_store_cached():
    """Verify that get_vector_store is cached."""
    # We need to mock JinaEmbeddings and Chroma inside app.db.vector to prevent real instantiation
    # Use patch on the module where get_vector_store is defined
    with (
        patch("app.db.vector.JinaEmbeddings") as mock_jina,
        patch("app.db.vector.Chroma") as mock_chroma,
    ):
        # We need to re-import or clear cache if it exists to test cleanly

        # Clear cache if it exists (for when we fix it)
        if hasattr(get_vector_store, "cache_clear"):
            get_vector_store.cache_clear()

        vs1 = get_vector_store()
        vs2 = get_vector_store()

        assert vs1 is vs2, "get_vector_store should return the same instance (cached)"

        assert mock_jina.call_count == 1, f"JinaEmbeddings initialized {mock_jina.call_count} times"
        assert mock_chroma.call_count == 1, f"Chroma initialized {mock_chroma.call_count} times"
