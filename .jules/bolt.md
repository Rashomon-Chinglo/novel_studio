## 2025-02-23 - Factory Caching
**Learning:** In the current architecture, expensive clients (ChatOpenAI, Chroma, JinaEmbeddings) were being re-instantiated on every call to their respective getters (`get_llm`, `get_vector_store`), leading to significant overhead on initialization.
**Action:** Use `@functools.cache` for singleton clients.
