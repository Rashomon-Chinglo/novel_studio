## 2024-05-24 - Cache Expensive External Client Initializations
**Learning:** Factory functions like `get_vector_store` and `get_llm` initialize external clients on every call if uncached. This leads to redundant network connections or expensive setups inside performance-critical paths (e.g., chains or vector operations).
**Action:** Always use `@functools.cache` for singleton-like dependencies or external client initializations to prevent unnecessary overhead across the application.
