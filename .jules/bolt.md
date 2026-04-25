## 2024-04-25 - [Client Initialization Bottleneck]
**Learning:** Factory functions like `get_llm()` and `get_vector_store()` were initializing new instances of expensive clients (`ChatOpenAI`, `Chroma`) on every call. In a LangChain architecture where chains frequently request these clients, this creates massive redundant overhead (connections, validations).
**Action:** Always apply `@functools.cache` to client factory functions to ensure they operate as singletons across the application lifecycle.
