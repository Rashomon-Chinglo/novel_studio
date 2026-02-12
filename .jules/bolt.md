## 2025-02-18 - [Vector Store Async Operations]
**Learning:** LangChain vector store methods like `add_texts` are synchronous and block the event loop, even inside async functions. This defeats the purpose of async operations around it (like `AsyncSessionLocal`).
**Action:** Always check for `aadd_texts` or `asimilarity_search` equivalents when working with LangChain vector stores in async contexts.
