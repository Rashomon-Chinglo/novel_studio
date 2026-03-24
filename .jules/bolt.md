## 2024-05-24 - [Cache Expensive Clients]
**Learning:** Factory functions initializing expensive clients (e.g., vector stores, LLMs in LangChain/ChromaDB) can become massive performance bottlenecks if they are called frequently and recreate connections or models each time.
**Action:** Always use `@functools.lru_cache` (or similar memoization techniques) on functions like `get_vector_store` and `get_llm` to ensure they act as singletons, reusing the initialized clients.
