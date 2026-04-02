## 2024-05-23 - Async Vector Store & Caching
**Learning:** `Chroma` and `JinaEmbeddings` initialization can be expensive and should be cached. More importantly, synchronous vector store operations (like `add_texts`) block the asyncio loop, devastating concurrency when using semaphores. Always check for async alternatives (`aadd_texts`) in LangChain integrations.
**Action:** Always verify if IO-bound operations in `async` functions are truly non-blocking. Use `lru_cache` for stateless service/client factories.
