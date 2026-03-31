from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models.snippet import Snippet


class SnippetRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, snippet_id: str) -> Snippet | None:
        return await self.session.get(Snippet, snippet_id)

    def add(self, snippet: Snippet) -> None:
        self.session.add(snippet)

    def add_many(self, snippets: Sequence[Snippet]) -> None:
        self.session.add_all(list(snippets))

    async def list_by_title(self, title: str) -> Sequence[Snippet]:
        result = await self.session.execute(
            select(Snippet).where(Snippet.title == title).order_by(Snippet.created_at.desc())
        )
        return result.scalars().all()
