
## 2025-03-02 - Caching Expensive Langchain Clients
**Learning:** Factory functions initializing expensive clients like LangChain's `Chroma` and `JinaEmbeddings`, or `ChatOpenAI`, can become significant performance bottlenecks if they are repeatedly called (e.g., inside loops or frequently accessed chains). Redundant recreation of these clients increases execution time immensely.
**Action:** Always verify if expensive clients are reused and implement singleton patterns or simple caching mechanisms like `@functools.lru_cache()` on their factory functions (`get_vector_store()`, `get_llm()`) to ensure single initialization per app lifecycle.
