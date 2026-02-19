## 2026-02-19 - Vector Store Initialization Cost
**Learning:** `JinaEmbeddings` and `Chroma` client initialization is synchronous and expensive (~250ms), blocking the main thread. Frequent calls (e.g., during startup or repeated tasks) without caching cause significant slowdown.
**Action:** Always use `@functools.lru_cache` for factories that initialize expensive clients like LLMs or Vector Stores to ensure singleton behavior.
