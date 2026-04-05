from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.repositories.materials import SnippetRepository
from app.persistence.repositories.outlines import (
    BibleRepository,
    ChapterBlueprintRepository,
    ChapterOutlineRepository,
    SubstoryRepository,
)
from app.persistence.repositories.post_writing import (
    ChapterSummaryRepository,
    CumulativeSubstorySummaryRepository,
)
from app.persistence.repositories.workflow import WorkflowRunRepository
from app.persistence.repositories.writing import WrittenChapterRepository


@dataclass(slots=True)
class OutlinesRepositoryGroup:
    bibles: BibleRepository
    substories: SubstoryRepository
    chapter_blueprints: ChapterBlueprintRepository
    chapter_outlines: ChapterOutlineRepository


@dataclass(slots=True)
class MaterialsRepositoryGroup:
    snippets: SnippetRepository


@dataclass(slots=True)
class PostWritingRepositoryGroup:
    chapter_summaries: ChapterSummaryRepository
    cumulative_substory_summaries: CumulativeSubstorySummaryRepository


@dataclass(slots=True)
class WorkflowRepositoryGroup:
    workflow_runs: WorkflowRunRepository


@dataclass(slots=True)
class WritingRepositoryGroup:
    written_chapters: WrittenChapterRepository


@dataclass(slots=True)
class RepositoryGroups:
    outlines: OutlinesRepositoryGroup
    materials: MaterialsRepositoryGroup
    post_writing: PostWritingRepositoryGroup
    workflow: WorkflowRepositoryGroup
    writing: WritingRepositoryGroup


def build_repository_groups(session: AsyncSession) -> RepositoryGroups:
    return RepositoryGroups(
        outlines=OutlinesRepositoryGroup(
            bibles=BibleRepository(session),
            substories=SubstoryRepository(session),
            chapter_blueprints=ChapterBlueprintRepository(session),
            chapter_outlines=ChapterOutlineRepository(session),
        ),
        materials=MaterialsRepositoryGroup(snippets=SnippetRepository(session)),
        post_writing=PostWritingRepositoryGroup(
            chapter_summaries=ChapterSummaryRepository(session),
            cumulative_substory_summaries=CumulativeSubstorySummaryRepository(session),
        ),
        workflow=WorkflowRepositoryGroup(workflow_runs=WorkflowRunRepository(session)),
        writing=WritingRepositoryGroup(written_chapters=WrittenChapterRepository(session)),
    )
