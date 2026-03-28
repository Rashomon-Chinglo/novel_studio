## 2024-05-24 - Cache Expensive Client Initialization
**Learning:** Factory functions initializing expensive clients like vector stores and LLMs can cause redundant initialization overhead and excessive connections if called multiple times per request or throughout the application lifecycle.
**Action:** Use caching (e.g., `@functools.lru_cache(maxsize=1)`) on functions that return expensive singleton-like clients (like `get_llm` and `get_vector_store`) to ensure they are instantiated only once, thereby preventing performance bottlenecks.
