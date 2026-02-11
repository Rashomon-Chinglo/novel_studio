## 2025-05-18 - Async Database & Caching
**Learning:** Initializing vector store clients (like `Chroma` with `JinaEmbeddings`) is expensive. Always cache factory functions using `@lru_cache` to ensure singleton behavior. Additionally, avoid blocking the event loop with synchronous vector DB calls; use `aadd_texts` instead of `add_texts`.
**Action:** When working with resource-heavy client initializations, check for caching. When writing async services, verify all I/O calls use their async counterparts.

## 2025-05-18 - Mocking SQLAlchemy AsyncSession
**Learning:** `AsyncSessionLocal` is often an `async_sessionmaker`, not the session itself. When mocking `async with AsyncSessionLocal() as session:`, you must mock the factory's `return_value` as the session object, and ensure that session object's `__aenter__` returns the actual session mock used in the block.
**Action:** Use precise mock chaining for async context managers: `mock_factory.return_value.__aenter__.return_value = mock_session`.
