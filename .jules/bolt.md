## 2026-06-26 - [Replace blocking add_texts with async aadd_texts]
**Learning:** The synchronous `add_texts` method in `langchain_chroma.Chroma` blocks the asyncio event loop when processing multiple snippets concurrently, reducing performance. Using `aadd_texts` avoids blocking.
**Action:** Always verify if external library methods used inside async functions block the event loop, and prefer async alternatives like `aadd_texts`.
