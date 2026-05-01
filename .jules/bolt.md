## 2024-05-01 - Cache expensive client factory initialization
**Learning:** Factory functions like `get_llm()` and `get_vector_store()` that initialize expensive third-party clients (OpenAI, Chroma, Embeddings) add significant overhead when called repeatedly.
**Action:** Use `@functools.cache` on factory functions that return stateless/reusable clients to ensure singleton instances and avoid redundant instantiation overhead.
