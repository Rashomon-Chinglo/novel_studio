## 2025-04-04 - [Cache Expensive Client Factory Functions]
**Learning:** Factory functions initializing expensive clients (e.g., `ChatOpenAI`, `Chroma`, `JinaEmbeddings`) are called multiple times across different modules (like in LangChain chain definitions), leading to redundant instantiations and potential performance bottlenecks.
**Action:** Use `@functools.cache` on factory functions like `get_llm()` and `get_vector_store()` to ensure singleton instances and avoid unnecessary overhead.
