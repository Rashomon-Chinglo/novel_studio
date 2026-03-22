## 2024-05-14 - Prevent Redundant Client Initialization
**Learning:** Factory functions `get_vector_store` and `get_llm` were creating new instances of expensive clients (ChromaDB and ChatOpenAI) on every invocation, causing significant performance overhead during repeated database or LLM calls.
**Action:** Use `@functools.lru_cache()` to cache singleton instances of expensive clients in factory functions, preventing redundant initialization.
