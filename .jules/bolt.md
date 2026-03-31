## 2024-05-23 - Synchronous Vector Store Blocking
**Learning:** The `Chroma` vector store client operations (like `add_texts`) are synchronous and block the asyncio event loop when called directly in async functions, degrading concurrency.
**Action:** Always wrap `vector_store` operations in `loop.run_in_executor` to offload them to a thread pool.
