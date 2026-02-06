from pydantic import BaseModel


class ChapterSummary(BaseModel):
    summary: str

    def prompt(self) -> str:
        return f"<章节总结>\n{self.summary}\n</章节总结>"


class CumulativeSubstorySummary(BaseModel):
    summary: str

    def prompt(self) -> str:
        return f"<卷内进度总结>\n{self.summary}\n</卷内进度总结>"
