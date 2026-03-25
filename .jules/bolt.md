
## 2025-03-25 - Cache Expensive Clients
**Learning:** Factory functions initializing expensive clients (e.g., vector stores, LLMs) can cause severe performance bottlenecks if called repeatedly, particularly when `get_vector_store` and `get_llm` are called per-request or per-operation.
**Action:** Always use `@functools.lru_cache(maxsize=1)` or similar singleton patterns to cache these expensive initializations, ensuring only a single instance of `Chroma`, `JinaEmbeddings`, or `ChatOpenAI` is created and reused.
