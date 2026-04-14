## 2024-05-18 - [Optimization] Cache Expensive Factories
**Learning:** Factory functions initializing expensive clients (e.g., vector stores, LLMs) must use caching (e.g., `@functools.cache`) to ensure singleton instances. Not doing so causes redundant initializations and severe performance bottlenecks in this specific architecture.
**Action:** Always add `@functools.cache` to factory functions providing LLM clients or Vector Stores.
