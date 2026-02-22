import os
import sys

# Add current directory to sys.path so we can import app
sys.path.append(os.getcwd())

# Mock environment variables before importing settings
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"

try:
    from app.db.vector import get_vector_store
except Exception as e:
    print(f"Failed to import: {e}")
    sys.exit(1)


def test_singleton():
    print("Testing get_vector_store singleton behavior...")
    store1 = get_vector_store()
    store2 = get_vector_store()

    if store1 is store2:
        print("✅ SUCCESS: Vector store is a singleton.")
    else:
        print("❌ FAILURE: Vector store is NOT a singleton.")
        sys.exit(1)


if __name__ == "__main__":
    test_singleton()
