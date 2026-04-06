## 2024-11-09 - Cache Expensive Client Initializations
**Learning:** Factory functions initializing expensive clients (e.g., vector stores, LLMs) in this architecture cause redundant overhead if not cached.
**Action:** Use `@functools.cache` on factory functions like `get_vector_store` and `get_llm` to ensure singleton instances and prevent performance bottlenecks.
