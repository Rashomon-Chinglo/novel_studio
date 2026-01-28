## 2026-01-28 - Batching Database Operations
**Learning:** In async applications handling LLM outputs, processing chunks individually and saving to DB concurrently creates excessive connection overhead. Batching results from `asyncio.gather` and performing a single bulk insert significantly reduces DB transactions (N -> 1) and network overhead for vector stores.
**Action:** Always check for opportunities to collect results from concurrent tasks and perform batch persistence instead of persisting within the worker task.
