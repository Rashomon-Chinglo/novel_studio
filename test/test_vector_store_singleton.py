import os
import sys

# Set dummy env vars for testing BEFORE imports
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"

# Add root to path so we can import app
sys.path.append(os.getcwd())

from app.db.vector import get_vector_store


def test_vector_store_singleton():
    """Verify that get_vector_store returns a singleton instance."""
    print("Testing get_vector_store singleton behavior...")

    try:
        store1 = get_vector_store()
        store2 = get_vector_store()

        if store1 is store2:
            print("PASS: get_vector_store returned the same instance.")
        else:
            print(
                f"FAIL: get_vector_store returned different instances. {id(store1)} != {id(store2)}"
            )
            sys.exit(1)

        # Also verify it's a Chroma instance
        from langchain_chroma import Chroma

        if isinstance(store1, Chroma):
            print("PASS: Instance is of type Chroma.")
        else:
            print(f"FAIL: Instance is not Chroma, but {type(store1)}.")
            sys.exit(1)

    except Exception as e:
        print(f"FAIL: Exception occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_vector_store_singleton()
