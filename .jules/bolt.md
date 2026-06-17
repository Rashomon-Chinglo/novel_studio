## 2025-02-12 - Cache LLM and Vector Store clients
**Learning:** LangChain clients like `ChatOpenAI` and `Chroma` are thread-safe and can be reused. In this architecture, factory functions like `get_llm()` and `get_vector_store()` were creating new client instances on every call, leading to memory overhead and unnecessary initialization latency.
**Action:** Implemented caching on expensive client factories using `@functools.cache`. This ensures singletons are returned across the application, saving resources and speeding up processes that request these clients repeatedly.
