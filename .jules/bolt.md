
## 2026-04-21 - [Optimize Client Initialization]
**Learning:** The project relies on multiple expensive clients like `Chroma` for vector stores and `ChatOpenAI` for LLMs. These are retrieved using factory functions (`get_vector_store` and `get_llm`), which were instantiating new client objects upon every call. This causes redundant object initialization overhead and potentially excessive connection handling under load.
**Action:** Always wrap application-level expensive resource providers or client factory functions with `@functools.cache` to enforce a singleton pattern and prevent redundant instantiations, unless distinct instances are strictly required by the use case.
