## 2024-05-19 - Cache Expensive Client Initializations
**Learning:** LangChain clients like `ChatOpenAI` and `Chroma` (along with their underlying `JinaEmbeddings`) are expensive to initialize and often thread-safe for stateless usage. Creating new instances for every request/operation adds unnecessary I/O overhead and increases memory footprint.
**Action:** Always use `@functools.cache` on factory functions like `get_llm()` and `get_vector_store()` to ensure singleton instances across the application, preventing redundant initializations.
