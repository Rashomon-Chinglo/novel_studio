import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest  # type: ignore

# Set dummy env vars for imports
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"

from app.modules.materials.schemas import MaterialSnippet
from app.service.materials import MaterialService


@pytest.mark.asyncio
async def test_save_snippets_uses_async_add_texts():
    with (
        patch("app.service.materials.get_vector_store") as mock_get_vs,
        patch("app.service.materials.AsyncSessionLocal") as mock_session_cls,
        patch("app.service.materials.MaterialEngine"),
    ):
        # Setup Mock Vector Store
        mock_vs = MagicMock()
        mock_vs.add_texts = MagicMock()
        mock_vs.aadd_texts = AsyncMock()
        mock_get_vs.return_value = mock_vs

        # Setup Mock Session
        # AsyncSessionLocal() returns a session which is an async context manager
        mock_session_instance = MagicMock()
        mock_session_cls.return_value = mock_session_instance

        # When entering the session context manager, return the session itself
        mock_session_context = AsyncMock()
        # session.add_all is synchronous
        mock_session_context.add_all = MagicMock()
        mock_session_instance.__aenter__.return_value = mock_session_context

        # session.begin() is a SYNC method that returns an async context manager
        mock_transaction_cm = AsyncMock()
        mock_session_context.begin = MagicMock(return_value=mock_transaction_cm)
        mock_transaction_cm.__aenter__.return_value = AsyncMock()

        # Instantiate Service
        service = MaterialService()

        # Create dummy data
        snippets = [
            MaterialSnippet(
                category="对话", tags=["tag1"], mood="喜悦", essential_text="some content"
            )
        ]

        # Run method
        await service.save_snippets("Test Title", snippets)

        # Verify aadd_texts was called
        mock_vs.aadd_texts.assert_called_once()
        # Verify add_texts was NOT called
        mock_vs.add_texts.assert_not_called()
