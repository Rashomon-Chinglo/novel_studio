import os
import sys
import unittest
from unittest.mock import patch

# Ensure app can be imported
sys.path.append(os.getcwd())

# Set dummy env vars
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"

from app.db.vector import get_vector_store


class TestVectorStoreSingleton(unittest.TestCase):
    @patch("app.db.vector.JinaEmbeddings")
    @patch("app.db.vector.Chroma")
    def test_get_vector_store_singleton(self, mock_chroma, mock_jina):
        # clear cache if exists (to be safe if running multiple tests)
        if hasattr(get_vector_store, "cache_clear"):
            get_vector_store.cache_clear()

        # Call get_vector_store twice
        store1 = get_vector_store()
        store2 = get_vector_store()

        # Verify that they are the same instance
        self.assertIs(store1, store2, "get_vector_store should return the same instance")

        # Verify that JinaEmbeddings and Chroma were instantiated only once
        mock_jina.assert_called_once()
        mock_chroma.assert_called_once()


if __name__ == "__main__":
    unittest.main()
