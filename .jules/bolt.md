## 2024-04-12 - Expensive Client Initialization
**Learning:** Langchain LLM and Vector Store clients are expensive to initialize and should not be re-instantiated on every call.
**Action:** Always use `@functools.cache` or similar singleton patterns on client factory functions like `get_llm` and `get_vector_store`.
