## 2023-10-24 - Async Vector DB Sync I/O Blocking Workaround
**Learning:** Langchain chroma vector store `add_texts` method is synchronous, which can block the event loop in `asyncio` parallel workers (like `process_content` in `MaterialService`).
**Action:** When invoking langchain/chroma DB operations inside async workers or tasks, explicitly use the `aadd_texts` or async variants to ensure the event loop is not blocked and concurrency works effectively.
