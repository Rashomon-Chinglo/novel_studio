
## 2024-03-03 - Resource Initialization & Async DB Writes
**Learning:** Found that factory functions like `get_vector_store` and `get_llm` were not using `@functools.lru_cache`, which would result in redundant TCP connection setups and object creation overhead per invocation. Also found that `Chroma`'s `add_texts` method was called synchronously within an async flow, blocking the `asyncio` loop.
**Action:** Use `@functools.lru_cache` for expensive singleton dependencies like DB clients and LLMs. Always use asynchronous equivalents (e.g., `aadd_texts`) instead of their synchronous counterparts when running inside `async` contexts.
