## 2024-05-24 - [Avoid Redundant Client Initialization in Factory Functions]
**Learning:** Factory functions initializing expensive clients like vector stores or LLMs (e.g., `get_vector_store`, `get_llm`) can become silent performance bottlenecks if called multiple times, as they recreate expensive network connections and re-instantiate heavy objects each time.
**Action:** Use `@functools.cache` on these factory functions to ensure singleton instances are returned, avoiding redundant initialization and saving both CPU cycles and network latency.
