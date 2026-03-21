## 2024-05-24 - Cache factory functions for expensive clients
**Learning:** Factory functions like `get_vector_store` and `get_llm` initialize expensive clients (Vector stores, LLMs). Calling them repeatedly in loops or per-request without caching causes unnecessary overhead and instantiates multiple redundant clients.
**Action:** Use `@functools.lru_cache` to ensure singleton instances for expensive clients in `app/db/vector.py` and `app/core/llm.py`.
