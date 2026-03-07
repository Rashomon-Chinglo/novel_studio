## 2024-03-24 - Cache Expensive Factory Functions
**Learning:** Factory functions initializing expensive clients like `Chroma` and `ChatOpenAI` are called multiple times in chains and modules without caching. This redundantly instantiates heavy clients in `app/core/llm.py` and `app/db/vector.py`.
**Action:** Always wrap heavy client factory functions with `@functools.lru_cache()` to enforce singleton instances and improve performance.
