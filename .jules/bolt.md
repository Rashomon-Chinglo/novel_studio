## 2025-01-29 - Synchronous Vector Store Writes Block Async Loop
**Learning:** `Chroma.add_texts` (and potentially other LangChain vector stores) is synchronous and blocks the asyncio event loop when called within an async function. This negates the benefits of `asyncio.gather` for concurrent processing.
**Action:** When using synchronous vector store methods in an async pipeline, ensure they are batched to minimize blocking time, or run them in a thread pool executor.
