import os
import sys

# Set dummy env vars before importing app modules that use settings
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"

# Add root to path since we are running as a script
sys.path.append(os.getcwd())

from app.db.vector import get_vector_store


def test_vector_store_is_singleton():
    """Verify that get_vector_store returns the same instance on subsequent calls."""
    try:
        store1 = get_vector_store()
        store2 = get_vector_store()

        if store1 is store2:
            print("✅ PASS: Vector store is a singleton")
        else:
            print("❌ FAIL: Vector store returned different instances")
            sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_vector_store_is_singleton()
