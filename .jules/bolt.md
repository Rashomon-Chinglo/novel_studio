## 2026-06-30 - Optimize LLM and Vector Store Initialization
**Learning:** Factory functions initializing expensive clients like `ChatOpenAI` and `Chroma` were creating new instances on every call, leading to unnecessary I/O and memory overhead.
**Action:** Use `@functools.cache` on `get_llm()` and `get_vector_store()` factory functions to implement them as cached singletons, minimizing initialization bottlenecks.
