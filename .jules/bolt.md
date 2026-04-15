## 2024-04-15 - [Cache Expensive Factory Functions]
**Learning:** Factory functions that initialize expensive clients like LangChain's `ChatOpenAI` and `Chroma` vector stores (which intern initialize embeddings like `JinaEmbeddings`) can become severe performance bottlenecks if called repeatedly, leading to redundant network calls and memory usage.
**Action:** Always wrap these factory functions (e.g., `get_llm`, `get_vector_store`) with `@functools.cache` to enforce a singleton pattern and reuse the client instances across the application lifecycle.
