
## 2024-05-24 - Cache Expensive Factory Initializations
**Learning:** Factory functions initializing expensive clients (e.g., Chroma DB, OpenAI Chat) cause performance bottlenecks due to redundant initialization when called repeatedly.
**Action:** Use `@functools.lru_cache(maxsize=1)` to enforce a singleton pattern for expensive service initializations.
