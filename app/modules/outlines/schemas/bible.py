from pydantic import BaseModel, Field


class Bible(BaseModel):
    title: str = Field(alias="书名", description="书名")
    logline: str = Field(
        alias="梗概",
        description="梗概，一句话梗概（尽量做到引人眼球，30-50字，必须包含钩子）",
    )

    marketing_hook: str = Field(alias="核心卖点，爽点", description="核心卖点，爽点")
    worldview_tone: str = Field(
        alias="世界观基调",
        description="世界观基调，例如[赛博休闲]，[女尊恋爱]，[无限流]等",
    )
    main_conflict: str = Field(alias="主线冲突", description="主线冲突")
    ending_vision: str = Field(alias="结局愿景", description="结局愿景")

    key_roles_summary: str = Field(
        alias="主角们的简要概述", description="主角们的简要概述"
    )

    def prompt(self, exclude: list[str] = []):
        bible = self.model_dump(exclude=exclude, exclude_none=True, by_alias=True)

        content = "\n\n".join([f"## {k}\n{v}" for k, v in bible.items()])
        return f"<小说总纲>\n{content}\n</小说总纲>"
