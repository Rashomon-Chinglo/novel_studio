## 2025-02-23 - Async I/O for Chroma Vector Store
**Learning:** Calling synchronous methods like `add_texts` on Chroma vector store within an async function like `save_snippets` blocks the main event loop, causing severe performance issues.
**Action:** Always use the asynchronous equivalent `aadd_texts` for I/O operations involving vector stores in async contexts.
