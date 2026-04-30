## 2024-05-18 - Cache Expensive Client Initialization
**Learning:** Factory functions initializing expensive clients like LangChain's ChatOpenAI and Chroma DB instances run synchronously and cause significant performance bottlenecks if repeatedly called without caching, leading to redundant network calls and high initialization overhead.
**Action:** Always wrap expensive client factory functions (e.g., `get_llm()`, `get_vector_store()`) with `@functools.cache` to ensure they function as singletons across the application lifecycle.
