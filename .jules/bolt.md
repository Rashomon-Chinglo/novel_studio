## 2024-05-23 - [Uncached Vector Store Initialization]
**Learning:** `get_vector_store` was re-initializing `JinaEmbeddings` and `Chroma` on every call. This is a common pattern to watch out for in factory functions.
**Action:** Always check if expensive client initializations (DB, AI models) are cached or singletons.
