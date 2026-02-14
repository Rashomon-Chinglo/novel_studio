## 2024-05-23 - Heavy Client Factory Anti-Pattern
**Learning:** Factory functions like `get_vector_store` that initialize heavy clients (Chroma, JinaEmbeddings) should always be cached (e.g., `@functools.lru_cache`).
**Action:** When seeing `get_X()` functions for database or API clients, check if they return a new instance every time. If so, and the client is stateless/thread-safe, cache it.
