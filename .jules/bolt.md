
## 2025-02-23 - Prevent Redundant Client Init & Blocking Calls
**Learning:** Factory functions returning expensive objects like ChatOpenAI or Chroma instances must be cached with `@functools.lru_cache` if called repeatedly across the application. Furthermore, calling blocking I/O methods like `add_texts` in async contexts creates a massive bottleneck.
**Action:** Always wrap heavy client factories in `lru_cache`, and aggressively search for synchronous I/O operations in `async def` functions, replacing them with their `a`-prefixed async counterparts (e.g. `aadd_texts`).
