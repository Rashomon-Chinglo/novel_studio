## 2025-02-28 - Optimizing Vector Store Access
**Learning:** `get_vector_store` was creating a new `Chroma` client instance on every call, which adds measurable overhead (~5ms/call locally, likely more if remote).
**Action:** Use `@functools.lru_cache` for factory functions that return expensive clients like database connections or API clients.

## 2025-02-28 - Async Vector Operations
**Learning:** `Chroma.add_texts` is a synchronous blocking operation. In an async context (`app/service/materials.py`), this blocks the event loop.
**Action:** Always check if the library provides async alternatives (e.g., `aadd_texts`) when working in `async def` functions to maintain concurrency.
