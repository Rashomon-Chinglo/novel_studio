## 2024-03-29 - [Cache Client Singletons]
**Learning:** Instantiating `ChatOpenAI` and `Chroma`/`JinaEmbeddings` repeatedly per request creates significant overhead. In LangChain setups with multiple chains or frequent API calls, recreating these client objects blocks the execution and burns CPU unnecessarily.
**Action:** Use `@functools.lru_cache` to memoize client instances like `get_llm()` and `get_vector_store()`.
