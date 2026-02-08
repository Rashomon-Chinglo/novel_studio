## 2024-05-23 - [Caching Vector Store Initialization]
**Learning:** Factory functions that initialize expensive clients (like `Chroma` and `JinaEmbeddings`) should be cached to avoid redundant initializations, especially when called frequently (e.g., in service instantiation).
**Action:** Use `@functools.lru_cache` (or `lru_cache()`) on factory functions that return stateless or long-lived client objects.
