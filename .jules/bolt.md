## 2024-05-18 - [Optimize Client Instantiation]
**Learning:** Factory functions initializing expensive clients (like vector stores or LLMs) should use caching to avoid redundant initializations and potential performance bottlenecks.
**Action:** Always use `@functools.lru_cache` (or similar caching mechanisms) on factory functions that return expensive client instances.