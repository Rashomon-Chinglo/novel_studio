## 2024-06-13 - [LLM/Chroma Client Initialization Bottleneck]
**Learning:** Instantiating LangChain's `Chroma` and `ChatOpenAI` multiple times across the application causes substantial performance degradation, primarily due to redundant file I/O (Chroma SQLite initializations) and repeated instantiation memory overhead in the `get_llm` and `get_vector_store` functions.
**Action:** Use Python's `@functools.cache` decorator on client instantiation functions (e.g., `get_llm`, `get_vector_store`) to ensure these thread-safe singletons are initialized only once per application lifecycle.
