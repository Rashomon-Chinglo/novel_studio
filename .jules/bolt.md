## 2024-06-09 - Asyncio Event Loop Blocking by Synchronous Langchain Clients
**Learning:** In `MaterialService`, using the synchronous `add_texts` method of the `Chroma` vector store client blocks the asyncio event loop during material processing, creating a significant performance bottleneck when handling concurrent chunks.
**Action:** Always prefer the asynchronous variants (e.g., `aadd_texts`) of Langchain/Chroma client methods within async contexts (`async def`) to maintain non-blocking I/O operations.
