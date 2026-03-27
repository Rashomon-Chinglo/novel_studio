## 2025-05-18 - [Vector Store Initialization Overhead]
**Learning:** `get_vector_store` was creating new `JinaEmbeddings` and `Chroma` clients on every call. This added significant overhead (~44ms per call locally, likely more in prod) and wasted resources.
**Action:** Use `@functools.lru_cache` on factory functions that return heavy, stateless (or connection-pooled) clients like vector stores or LLMs.
