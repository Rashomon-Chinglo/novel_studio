## 2025-02-18 - Non-blocking async vector store ops
**Learning:** LangChain Chroma client methods like `add_texts` are synchronous and block the asyncio event loop during I/O. For heavy, batch operations (e.g., in `MaterialService.process_content`), this can severely degrade performance.
**Action:** Always use the asynchronous equivalent methods (e.g., `aadd_texts`) when interacting with vector stores or LLM clients inside an `async def` function.
