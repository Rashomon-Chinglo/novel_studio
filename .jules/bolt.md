## 2024-05-01 - Singleton Initialization for Expensive Clients
**Learning:** Factory functions that initialize expensive clients like LLMs (`ChatOpenAI`) and Vector Stores (`Chroma`, `JinaEmbeddings`) can become severe performance bottlenecks if they create new client instances on every call, particularly during request processing or heavy async tasks.
**Action:** Always use `@functools.cache` or equivalent memoization for singleton factories (`get_llm()`, `get_vector_store()`) to prevent redundant initializations and reuse connections.
