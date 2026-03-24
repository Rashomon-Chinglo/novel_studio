from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary

from .chain import get_chapter_summary_chain, get_cumulative_substory_summary_chain
from .context import ChapterSummaryContext, SubstoryCumulativeSummaryContext
from .prompt import ChapterSummaryPrompt, SubstoryCumulativeSummaryPrompt


class PostWritingEngine:
    ChapterSummaryContext = ChapterSummaryContext
    SubstoryCumulativeSummaryContext = SubstoryCumulativeSummaryContext

    def __init__(self):
        self.chapter_summary_prompt = ChapterSummaryPrompt()
        self.chapter_summary_llm = get_chapter_summary_chain(self.chapter_summary_prompt.prompt)
        self.substory_cumulative_summary_prompt = SubstoryCumulativeSummaryPrompt()
        self.substory_cumulative_summary_llm = get_cumulative_substory_summary_chain(
            self.substory_cumulative_summary_prompt.prompt
        )

    async def chapter_summary(self, context: ChapterSummaryContext) -> ChapterSummary:
        variables = self.chapter_summary_prompt.build_variables(context)
        summary = await self.chapter_summary_llm.ainvoke(variables)
        return ChapterSummary(summary=summary)

    async def cumulative_substory_summary(
        self, context: SubstoryCumulativeSummaryContext
    ) -> CumulativeSubstorySummary:
        variables = self.substory_cumulative_summary_prompt.build_variables(context)
        summary = await self.substory_cumulative_summary_llm.ainvoke(variables)
        return CumulativeSubstorySummary(summary=summary)
