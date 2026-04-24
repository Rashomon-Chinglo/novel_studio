
## 2024-04-24 - Cache expensive factory clients to prevent initialization overhead and redundant API calls
**Learning:** Factory methods like `get_vector_store` and `get_llm` were re-initializing clients (e.g., `JinaEmbeddings`, `ChatOpenAI`) on every call. This resulted in significant performance hits (e.g., >0.2s for vector store and >0.4s for LLM per call) and unnecessary resource utilization due to lack of caching.
**Action:** Use `@functools.cache` on factory functions that return external clients or large objects (e.g., vector stores, LLMs) to ensure they act as singletons, drastically cutting down initialization time to ~0.0002s and saving memory.

## 2024-04-24 - Prevent Event Loop Blocking in Async Applications
**Learning:** Using synchronous I/O operations, such as `add_texts` in LangChain Chroma, within `async` functions (like `save_snippets`) blocks the entire asyncio event loop, causing severe performance degradation in high-concurrency environments.
**Action:** Always favor asynchronous implementations (like `aadd_texts`) when working within an async context to maintain event loop responsiveness.
