import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

# Mock settings
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"

from app.db.vector import get_vector_store


def test_singleton():
    """Verify that get_vector_store returns the same instance (singleton)."""
    try:
        # First call
        store1 = get_vector_store()
        # Second call
        store2 = get_vector_store()

        # Check if they are the same object
        if store1 is store2:
            print("✅ get_vector_store returns the same instance.")
        else:
            print("❌ get_vector_store returns DIFFERENT instances.")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_singleton()
