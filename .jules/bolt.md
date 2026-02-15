## 2024-05-23 - Async Vector Store & Package Structure
**Learning:**
1.  **Package Structure:** Missing `__init__.py` files in subdirectories caused `pytest` import errors (`ModuleNotFoundError`). Converting directories to regular packages by adding `__init__.py` fixed test discovery and imports.
2.  **Vector Store Performance:** `Chroma` client initialization has significant overhead (~200ms). Using `@functools.lru_cache` on the factory function eliminates this cost for subsequent calls (reducing to ~90ns).
3.  **Blocking I/O:** `Chroma.add_texts` is synchronous and blocks the event loop. In async contexts, always use `await Chroma.aadd_texts` to allow concurrency.

**Action:**
- Ensure all module directories have `__init__.py` for proper testing.
- Always cache expensive client initializations.
- Prefer async methods for vector store operations in async services.
