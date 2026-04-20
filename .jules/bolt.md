## 2024-05-24 - Cache Expensive Client Initializations
**Learning:** Factory functions initializing expensive external clients like LangChain's `ChatOpenAI` and `Chroma` / `JinaEmbeddings` were lacking singleton patterns. Without this, repeated queries cause redundant setup overhead which becomes a significant performance bottleneck.
**Action:** Always verify if functions returning clients (e.g., `get_llm`, `get_vector_store`) use `@functools.cache` or another singleton pattern in this codebase.
