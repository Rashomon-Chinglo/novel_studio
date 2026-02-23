## 2024-05-22 - [Vector Store Initialization Cache]
**Learning:** `get_vector_store` was creating a new `Chroma` client on every call, which involves file I/O and embedding model initialization. This is a significant bottleneck if the function is called frequently (e.g., per request or in loops).
**Action:** Always check if expensive initialization functions are cached (singleton pattern) using `@functools.lru_cache` or similar mechanisms. Added `@lru_cache` to `get_vector_store`.
