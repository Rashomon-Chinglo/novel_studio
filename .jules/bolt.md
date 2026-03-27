# Bolt's Journal

## 2025-05-23 - [JinaEmbeddings + Chroma Initialization Overhead]
**Learning:** Initializing `JinaEmbeddings` and `Chroma` clients inside a function call (`get_vector_store`) without caching creates significant overhead (~0.65s for 50 calls vs ~0.29s cached). This is because it re-validates settings and potentially sets up new HTTP sessions/connections on every call.
**Action:** Always wrap expensive client factory functions with `@functools.lru_cache` (or `st.cache_resource` in Streamlit) to ensure they are singletons.
