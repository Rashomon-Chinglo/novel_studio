
## 2024-05-18 - Async Vector Store Insertion
**Learning:** Using synchronous `add_texts` from Langchain ChromaDB inside an async process blocks the main event loop and introduces a severe performance bottleneck.
**Action:** Always prefer `await aadd_texts` for vector store insertions in async contexts to prevent blocking the event loop and enable efficient concurrent processing.
