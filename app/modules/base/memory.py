from pydantic import BaseModel


class ChapterSummary(BaseModel):
    summary: str

    def prompt(self) -> str:
        if not self.summary.strip():
            return "<章节总结>\n暂无历史章节总结\n</章节总结>"
        return f"<章节总结>\n{self.summary}\n</章节总结>"


class CumulativeSubstorySummary(BaseModel):
    summary: str

    def prompt(self) -> str:
        if not self.summary.strip():
            return "<卷内进度总结>\n暂无卷内历史总结\n</卷内进度总结>"
        return f"<卷内进度总结>\n{self.summary}\n</卷内进度总结>"
