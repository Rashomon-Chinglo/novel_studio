## 2024-03-01 - Blocking I/O inside `asyncio.gather` prevents concurrency
**Learning:** Calling blocking external operations (like Chroma's synchronous `add_texts` method) within an `asyncio` context halts the event loop, completely negating the benefit of using `asyncio.gather` or semaphores for concurrent chunk processing.
**Action:** Always check the underlying implementation of vector store or API client methods when working inside an `asyncio` function. Ensure that strictly asynchronous equivalents (like `aadd_texts`) are used to allow proper context switching and true concurrency.

## 2024-03-01 - Redundant Vector Store / LLM Client Instantiation
**Learning:** Factory functions that create external clients, like `JinaEmbeddings` or `Chroma`, can introduce heavy I/O and object creation overhead per-request if they are not cached.
**Action:** Always use `@functools.lru_cache` (or equivalent singleton patterns) for factory functions that return expensive client wrappers to guarantee reuse across requests.
