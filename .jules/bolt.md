## 2026-05-18 - Async LangChain Operations
**Learning:** Synchronous LangChain operations (like `add_texts` in `Chroma`) can block the asyncio event loop during I/O operations, leading to performance bottlenecks in async contexts like `MaterialService`.
**Action:** Always prefer the `a`-prefixed async versions of LangChain methods (e.g., `aadd_texts`, `ainvoke`) when operating within async functions to allow proper concurrency. When testing these methods, remember to implement the async equivalents in mock classes.
