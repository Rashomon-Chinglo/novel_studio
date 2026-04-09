
## 2024-04-09 - Caching Expensive Client Initializations
**Learning:** Factory functions that initialize expensive external clients (like `ChatOpenAI`, `JinaEmbeddings`, or `Chroma`) are called multiple times across the application (e.g., in `MaterialService` and various generation chains). Without caching, this leads to redundant network requests or expensive client setup.
**Action:** Always use `@functools.cache` on factory functions like `get_llm()` or `get_vector_store()` to ensure they act as singletons, reducing latency and memory footprint.
