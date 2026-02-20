import os
import sys

# Set dummy env vars before importing anything that uses settings
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from app.db.vector import get_vector_store
except Exception as e:
    print(f"Import failed: {e}")
    sys.exit(1)


def test_singleton():
    print("Calling get_vector_store() first time...")
    try:
        store1 = get_vector_store()
    except Exception as e:
        print(f"Failed to create store1: {e}")
        return

    print(f"Store 1 id: {id(store1)}")

    print("Calling get_vector_store() second time...")
    try:
        store2 = get_vector_store()
    except Exception as e:
        print(f"Failed to create store2: {e}")
        return

    print(f"Store 2 id: {id(store2)}")

    if store1 is store2:
        print("SUCCESS: get_vector_store returns the same instance.")
    else:
        print("FAILURE: get_vector_store returns different instances.")


if __name__ == "__main__":
    test_singleton()
