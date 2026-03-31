## 2026-02-17 - Vector Store Re-initialization Overhead
**Learning:** Factory functions like `get_vector_store` that initialize heavy clients (JinaEmbeddings, Chroma) were being re-created on every call, adding ~47ms of latency.
**Action:** Always check factory functions in `app/db` and apply `@functools.lru_cache` to ensure singleton behavior for expensive clients.
