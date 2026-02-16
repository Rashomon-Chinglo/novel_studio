# BOLT'S JOURNAL

## 2024-03-24 - Vector Store Initialization Overhead
**Learning:** `get_vector_store` initializes `JinaEmbeddings` and `Chroma` client on every call, taking ~8.5ms. Since it's a stateless factory, caching it reduces call time to ~97ns.
**Action:** Always check expensive client initializations in factory functions and use `@functools.lru_cache` (or singleton pattern) if appropriate.

## 2024-03-24 - Async Vector Store Operations
**Learning:** `Chroma` vector store has synchronous `add_texts` and asynchronous `aadd_texts`. Using `add_texts` in an async function blocks the event loop, especially critical when processing multiple chunks concurrently.
**Action:** Always verify if library methods have async counterparts when working in async contexts (e.g., `langchain_chroma`).
