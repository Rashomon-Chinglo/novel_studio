import os
import sys
import unittest

# Add project root to path
sys.path.append(os.getcwd())

# Mock settings
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"
os.environ["DATA_DIR"] = "./app/data"

try:
    from app.db.vector import get_vector_store
except ImportError:
    pass


class TestVectorStoreSingleton(unittest.TestCase):
    def test_singleton(self):
        store1 = get_vector_store()
        store2 = get_vector_store()

        # Current behavior: they are different instances
        # Proposed behavior: they are the same instance

        # Check if they are the same object
        is_same = store1 is store2
        print(f"Are instances same? {is_same}")

        # With lru_cache, this should be True.
        # Without it, it should be False (unless Chroma has internal caching, but wrapper is new)

        self.assertTrue(is_same, "get_vector_store should return the same instance")


if __name__ == "__main__":
    unittest.main()
