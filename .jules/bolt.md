# Bolt's Journal ⚡

## 2024-05-22 - [Vector Store Initialization]
**Learning:** `get_vector_store` was re-initializing `JinaEmbeddings` and `Chroma` clients on every call (taking ~0.16s), which accumulates quickly in loops or high-traffic endpoints.
**Action:** Always check for expensive client initializations in factory functions and apply `@lru_cache` or singleton pattern. Also, verify that async methods (`aadd_texts`) are used for I/O bound operations to avoid blocking the event loop.
