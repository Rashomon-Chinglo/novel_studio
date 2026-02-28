
## 2024-05-19 - Expensive Client Initialization Bottleneck
**Learning:** `get_vector_store` in `app/db/vector.py` was instantiating `JinaEmbeddings` and `Chroma` clients repeatedly without caching. This caused huge performance overheads every time a client required the vector store because `JinaEmbeddings` and `Chroma` are heavy dependencies.
**Action:** Use `@functools.lru_cache` on functions that return expensive client instances to ensure they act as singletons across the application lifecycle. Also, do not modify `pyproject.toml` or `uv.lock` directly without an instruction to do so.
