## 2024-05-19 - [Preventing Redundant Client Initialization]
**Learning:** Factory functions that initialize expensive clients (like LangChain LLMs and ChromaDB vector stores) can become performance bottlenecks if they are called repeatedly without caching, leading to unnecessary connections and high memory usage.
**Action:** Always wrap expensive factory functions with `@functools.cache` to ensure singleton instances are returned.
