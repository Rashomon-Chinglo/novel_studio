## 2024-05-23 - Client Instantiation Overhead
**Learning:** Found that expensive clients like `ChatOpenAI` and `Chroma` vector stores are re-instantiated multiple times because factory functions (`get_llm`, `get_vector_store`) lack caching, resulting in unnecessary memory usage and initialization overhead.
**Action:** Use `@functools.cache` on factory functions that initialize expensive singletons to improve performance.
