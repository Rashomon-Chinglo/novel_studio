## 2024-05-22 - Vector Store Initialization Cache
**Learning:** `JinaEmbeddings` and `Chroma` client initialization is expensive (~4.5ms warm). `get_vector_store` was creating new instances on every call.
**Action:** Use `@functools.lru_cache` for factory functions that return expensive, stateless (or reusable) clients.
