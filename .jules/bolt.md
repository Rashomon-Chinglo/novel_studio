## 2024-05-24 - Cached Expensive Client Initialization
**Learning:** Factory functions for expensive clients like LLMs (`ChatOpenAI`) and Vector Stores (`Chroma`) were creating new instances on every call, causing unnecessary overhead.
**Action:** Always use `@functools.cache` for singleton clients to ensure they are instantiated only once, avoiding redundant network setups and disk reads.
