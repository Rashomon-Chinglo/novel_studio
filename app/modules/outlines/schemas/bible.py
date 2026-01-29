from typing import ClassVar

from pydantic import BaseModel


class Bible(BaseModel):
    _prompt_labels: ClassVar[dict[str, str]] = {
        "title": "书名",
        "logline": "梗概",
        "marketing_hook": "核心卖点，爽点",
        "worldview_tone": "世界观基调",
        "main_conflict": "主线冲突",
        "ending_vision": "结局愿景",
        "key_roles_summary": "主角们的简要概述",
    }

    title: str
    logline: str
    marketing_hook: str
    worldview_tone: str
    main_conflict: str
    ending_vision: str
    key_roles_summary: str

    def prompt(self, exclude: set[str] | None = None) -> str:
        if exclude is None:
            exclude = set()
        data = self.model_dump(exclude=exclude, exclude_none=True)
        bible = {self._prompt_labels.get(k, k): v for k, v in data.items()}

        content = "\n\n".join([f"## {k}\n{v}" for k, v in bible.items()])
        return f"<小说总纲>\n{content}\n</小说总纲>"
