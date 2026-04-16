## 2024-05-14 - Factory Function Caching
**Learning:** Redundant initialization of expensive clients (like ChatOpenAI and Chroma) occurs if factory functions (`get_llm`, `get_vector_store`) aren't cached, creating unnecessary bottlenecks.
**Action:** Always use `@functools.cache` on factory functions that return expensive client instances unless explicit fresh instances are strictly required.
