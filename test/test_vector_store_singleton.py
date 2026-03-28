import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add repo root to path
sys.path.append(os.getcwd())

# Mock environment variables for config
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"

from app.db.vector import get_vector_store


class TestVectorStoreSingleton(unittest.TestCase):
    @patch("app.db.vector.JinaEmbeddings")
    @patch("app.db.vector.Chroma")
    def test_singleton_behavior(self, mock_chroma, mock_embeddings):
        # Mock return values
        mock_instance = MagicMock()
        mock_chroma.return_value = mock_instance

        # First call
        store1 = get_vector_store()

        # Second call
        store2 = get_vector_store()

        # Assertions
        self.assertIs(store1, store2, "get_vector_store() should return the same instance")

        # Verify constructor called only once
        mock_chroma.assert_called_once()
        mock_embeddings.assert_called_once()

        print("Vector store singleton test passed!")

if __name__ == "__main__":
    unittest.main()
