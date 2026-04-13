## 2023-10-25 - [Initialization of Expensive Clients]
**Learning:** Factory functions returning LLM and vector store instances create expensive new clients on every call without caching.
**Action:** Use `@functools.cache` on `get_llm` and `get_vector_store` to ensure singleton instances and avoid performance bottlenecks.