## 2024-05-23 - Heavy Client Initialization in Factory Functions
**Learning:** Factory functions like `get_vector_store` that initialize heavy clients (Chroma, JinaEmbeddings) were not cached, leading to ~4ms overhead per call. This accumulates significantly if called frequently.
**Action:** Always wrap client initialization functions with `@functools.lru_cache()` to ensure singleton behavior and avoid redundant I/O or network setup.
