import os
import sys
import time

# Add project root to path
sys.path.append(os.getcwd())

# Mock settings if needed
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"
os.environ["DATA_DIR"] = "./app/data"

try:
    from app.core.llm import get_llm
    from app.db.vector import get_vector_store
except ImportError:
    pass


def benchmark():
    # Warm up
    get_vector_store()
    get_llm()

    start_time = time.time()
    for _ in range(100):
        _ = get_vector_store()
    end_time = time.time()
    print(f"get_vector_store: Time taken for 100 calls: {end_time - start_time:.4f} seconds")

    start_time = time.time()
    for _ in range(100):
        _ = get_llm()
    end_time = time.time()
    print(f"get_llm: Time taken for 100 calls: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    benchmark()
