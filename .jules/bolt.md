## 2025-04-19 - Caching Client Initializations
**Learning:** Factory functions initializing expensive clients like `Chroma` and `ChatOpenAI` must use `@functools.cache` to prevent redundant initializations. Not caching them results in high overhead from repeated connections and potential database locking issues.
**Action:** Always verify if new factory methods creating connections or LLM clients use `@functools.cache` to share the singleton instances.
