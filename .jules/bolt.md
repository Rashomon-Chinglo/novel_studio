## 2026-02-03 - [Blocking Vector Store Calls]
**Learning:** The `Chroma` vector store wrapper from `langchain_chroma` exposes synchronous `add_texts` methods which can block the asyncio event loop, especially when combined with network-bound embeddings (Jina).
**Action:** Always prefer `await vector_store.aadd_texts(...)` or other async equivalents when working within async services (e.g., `MaterialService`).
