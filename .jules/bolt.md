## 2024-05-24 - Cache expensive client instantiations
**Learning:** Factory functions initializing expensive clients like ChatOpenAI and Chroma (along with its embedding model) are repeatedly called throughout the application without caching, leading to redundant instantiations. This is a common performance bottleneck in LLM apps.
**Action:** Use `@functools.lru_cache(maxsize=1)` on factory functions like `get_llm()` and `get_vector_store()` to ensure they behave as singletons.
