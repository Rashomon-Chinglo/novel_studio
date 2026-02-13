## 2026-02-13 - Expensive Client Initialization
**Learning:** Re-initializing database clients (ChromaDB + JinaEmbeddings) on every call causes measurable overhead (~4.6ms per call).
**Action:** Use `functools.lru_cache` for factory functions to cache the client instance (Singleton pattern) and avoid redundant I/O and object creation.
