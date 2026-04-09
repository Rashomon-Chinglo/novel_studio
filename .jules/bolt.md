## 2024-05-22 - [Synchronous Vector Store Operations Blocking Event Loop]
**Learning:** The codebase uses `langchain-chroma` and `JinaEmbeddings` synchronously within `async` service methods (e.g., `MaterialService`). These operations involve network calls and disk I/O, which block the `asyncio` event loop, severely impacting concurrent performance.
**Action:** Always wrap synchronous vector store methods (like `add_texts`, `add_documents`) in `loop.run_in_executor` when calling them from `async` functions to keep the event loop responsive.
