## 2024-05-28 - Cache Expensive Client Initializations
**Learning:** Factory functions initializing expensive clients like LangChain's `ChatOpenAI` and `Chroma` / `JinaEmbeddings` vector stores create a significant performance bottleneck if called repeatedly, as they are not cached by default and re-initialize connections/configurations.
**Action:** Use Python's `@functools.lru_cache()` to cache factory functions (e.g., `get_llm`, `get_vector_store`) in `app/core/llm.py` and `app/db/vector.py` to ensure singleton instances are created.
