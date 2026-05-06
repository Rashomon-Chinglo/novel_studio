## 2024-05-18 - Caching LLM and VectorStore instances
**Learning:** In `app/core/llm.py` and `app/persistence/db/vector.py`, factory functions `get_llm` and `get_vector_store` return a new instance of ChatOpenAI and Chroma each time they are called. This means that if multiple chains are instantiated, new instances of these clients are repeatedly created.
**Action:** Add `@functools.cache` to these factory functions to ensure they return a singleton instance, preventing redundant initialization of these clients.
