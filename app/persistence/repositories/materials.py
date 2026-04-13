from collections.abc import Sequence

from sqlalchemy import case, or_, select
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

    async def search(
        self,
        *,
        query: str | None = None,
        limit: int = 8,
        category: str | None = None,
        mood: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> Sequence[Snippet]:
        stmt = select(Snippet)

        if category is not None:
            stmt = stmt.where(Snippet.category == category)

        if mood is not None:
            stmt = stmt.where(Snippet.mood == mood)

        if tags:
            for tag in tags:
                stmt = stmt.where(Snippet.tags.like(f'%"{tag}"%'))

        if query:
            pattern = f"%{query}%"
            relevance = (
                case((Snippet.content.like(pattern), 4), else_=0)
                + case((Snippet.tags.like(pattern), 3), else_=0)
                + case((Snippet.category.like(pattern), 2), else_=0)
                + case((Snippet.mood.like(pattern), 1), else_=0)
            )
            stmt = stmt.where(
                or_(
                    Snippet.content.like(pattern),
                    Snippet.tags.like(pattern),
                    Snippet.category.like(pattern),
                    Snippet.mood.like(pattern),
                )
            ).order_by(relevance.desc(), Snippet.created_at.desc())
        else:
            stmt = stmt.order_by(Snippet.created_at.desc())

        result = await self.session.execute(stmt.limit(limit))
        return result.scalars().all()
