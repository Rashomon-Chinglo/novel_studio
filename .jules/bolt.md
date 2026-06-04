## 2024-05-15 - Event Loop Blocking with LangChain Sync Clients
**Learning:** Calling synchronous methods of LangChain clients (like `Chroma.add_texts`) inside `asyncio.gather` tasks blocks the event loop, causing concurrency bottlenecks in IO-bound operations (e.g., `MaterialService.process_content`).
**Action:** Always prefer the `a`-prefixed asynchronous methods (like `aadd_texts`) provided by LangChain components when operating within an async context to maintain event loop non-blocking behavior. Mock classes in tests must also implement these async methods.
