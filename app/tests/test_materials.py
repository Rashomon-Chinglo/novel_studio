import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Set dummy env vars for settings validation
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"
os.environ["CHROMA_COLLECTION_NAME"] = "dummy"
os.environ["CHROMA_URL"] = "dummy"

from app.modules.materials.schemas import MaterialSnippet
from app.service.materials import MaterialService


@pytest.mark.asyncio
async def test_save_snippets_uses_async_add_texts():
    # Setup mocks
    mock_vector_store = MagicMock()
    # Mock methods
    mock_vector_store.add_texts = MagicMock()
    mock_vector_store.aadd_texts = AsyncMock()

    # Mock AsyncSessionLocal
    mock_session = AsyncMock()
    # Mock begin() context manager
    mock_begin_cm = MagicMock()
    mock_begin_cm.__aenter__ = AsyncMock()
    mock_begin_cm.__aexit__ = AsyncMock()
    mock_session.begin.return_value = mock_begin_cm

    # Mock AsyncSessionLocal factory instance (the context manager)
    mock_session_cm = MagicMock()
    mock_session_cm.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_cm.__aexit__ = AsyncMock()

    # Mock AsyncSessionLocal callable
    mock_session_local_factory = MagicMock(return_value=mock_session_cm)

    # Patch dependencies
    with (
        patch("app.service.materials.get_vector_store", return_value=mock_vector_store),
        patch("app.service.materials.AsyncSessionLocal", side_effect=mock_session_local_factory),
        patch("app.modules.materials.engine.MaterialEngine"),
    ):
        service = MaterialService()

        snippets = [
            MaterialSnippet(category="动作", tags=["tag1"], mood="平静", essential_text="some text")
        ]

        await service.save_snippets("Test Title", snippets)

        # Verify add_texts was NOT called
        if mock_vector_store.add_texts.called:
            pytest.fail("Should use aadd_texts instead of add_texts (blocking call detected)")

        # Verify aadd_texts WAS called
        mock_vector_store.aadd_texts.assert_called_once()
