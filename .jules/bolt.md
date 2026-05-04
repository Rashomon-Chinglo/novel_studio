## 2026-05-04 - [Cache Expensive Factory Initializations]
**Learning:** Factory functions initializing expensive clients like LLMs and VectorStores (e.g., `ChatOpenAI`, `Chroma`, `JinaEmbeddings`) should be cached using `@functools.cache` to prevent redundant instantiations and networking overhead, especially in web frameworks where they might be fetched repeatedly per request.
**Action:** Always wrap application-level client factory functions (like `get_llm`, `get_vector_store`) with `@functools.cache` to make them singletons.
