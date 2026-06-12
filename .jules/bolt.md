## 2025-06-12 - Prevented Event Loop Blocking by Using Async Vector Store Writes

**Learning:** LangChain/ChromaDB clients expose both synchronous (e.g., `add_texts`) and asynchronous (e.g., `aadd_texts`) methods. Using the synchronous methods inside an async context (like in `MaterialService.save_snippets`) acts as a codebase-specific anti-pattern, because it blocks the asyncio event loop, defeating the purpose of asynchronous concurrent processing.

**Action:** Always verify if LangChain/ChromaDB clients expose an async variant (like `aadd_texts`) when working within an async context or event loop in this codebase, and strictly prefer it to prevent blocking the event loop during I/O operations.