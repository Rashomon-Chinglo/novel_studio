
## 2024-05-18 - Singleton Initialization of LangChain Clients
**Learning:** Initializing Langchain's `ChatOpenAI` and `Chroma` vector stores on every request is notoriously expensive. For `ChatOpenAI`, caching enables the underlying `httpx` client to reuse HTTP connections (connection pooling), significantly reducing latency. For `Chroma`, it prevents repeated, expensive initializations of the local sqlite database (via `chromadb.PersistentClient`), avoiding file locks and disk reads.
**Action:** Always use `@functools.cache` on factory functions that return expensive client instances like `ChatOpenAI`, `JinaEmbeddings`, or `Chroma` in this application architecture.
