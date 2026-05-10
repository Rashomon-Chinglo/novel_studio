
## 2024-05-24 - Async IO blocking via VectorStore
**Learning:** Chroma vector store's synchronous `add_texts` blocks the async event loop in concurrent operations like saving snippets.
**Action:** Always prefer `aadd_texts` over `add_texts` for Chroma and other Langchain vector stores in async contexts.
