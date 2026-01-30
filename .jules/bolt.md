## 2026-01-30 - Blocking Vector Store Operations
**Learning:** `langchain_chroma.Chroma.add_texts` is synchronous and blocks the asyncio event loop. In concurrent processing pipelines (like `asyncio.gather`), this serializes execution and kills performance.
**Action:** Always wrap `vector_store.add_texts` (and other synchronous I/O) in `loop.run_in_executor` or use batching to minimize blocking calls.
