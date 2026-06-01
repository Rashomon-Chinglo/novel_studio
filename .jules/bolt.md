## 2024-10-27 - Fix async event loop blocking in MaterialService
**Learning:** In the `MaterialService`, using an `asyncio.Semaphore(2)` is meant to limit concurrent background execution. However, using the synchronous `add_texts` method from `langchain_chroma.Chroma` blocks the event loop, causing unexpected I/O blockages inside an async loop and defeating the concurrency limit.
**Action:** Use `await aadd_texts` in async contexts to prevent event loop blocking during heavy I/O operations.
