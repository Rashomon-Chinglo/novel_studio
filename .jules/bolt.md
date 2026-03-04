
## 2026-03-04 - Prevent Redundant Client Instantiation
**Learning:** Langchain tools like ChatOpenAI and Chroma stores instantiate clients (and embeddings models) under the hood. Repeatedly calling factory functions like `get_llm()` or `get_vector_store()` re-creates these instances, causing unnecessary API latency, memory overhead, and duplicate API connections.
**Action:** Use `@functools.lru_cache` (or `@functools.cache`) on factory functions that build external clients or expensive dependencies to ensure singleton behavior within the application lifecycle.
