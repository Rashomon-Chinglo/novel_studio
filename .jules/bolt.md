## 2024-04-18 - Cache Expensive Client Initializations
**Learning:** Factory functions initializing expensive clients (e.g., vector stores, LLMs) in this architecture cause redundant initializations if not cached, impacting performance during repeated calls across different modules.
**Action:** Always use `@functools.cache` (or similar memoization) on factory functions like `get_llm()` and `get_vector_store()` to ensure singleton instances are returned and to prevent redundant overhead.
