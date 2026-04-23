## 2024-05-18 - Cache expensive client initializations
**Learning:** Factory functions like `get_llm()` and `get_vector_store()` that initialize expensive clients (like OpenAI, Chroma, JinaEmbeddings) can cause significant overhead and memory leaks if called repeatedly without caching, as they instantiate a new client every time.
**Action:** Always use `@functools.cache` on such factory functions to enforce a singleton pattern and prevent redundant initialization.
