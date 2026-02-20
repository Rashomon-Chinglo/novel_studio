## 2024-05-22 - [Singleton Pattern for Heavy Clients]
**Learning:** `get_vector_store` was initializing `Chroma` and `JinaEmbeddings` clients on every call, leading to redundant file I/O and connection setup.
**Action:** Always check if client initialization functions (like for databases or LLMs) are cached. Use `@functools.lru_cache` to enforce singleton behavior for stateless client factories.
