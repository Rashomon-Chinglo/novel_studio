import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

# Mock settings if needed
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"
os.environ["DATA_DIR"] = "./app/data"

from app.db.vector import get_vector_store


def verify_singleton():
    store1 = get_vector_store()
    store2 = get_vector_store()

    if store1 is store2:
        print("✅ get_vector_store returns the same instance (Singleton)")
    else:
        print("❌ get_vector_store returns different instances")
        exit(1)


if __name__ == "__main__":
    verify_singleton()
