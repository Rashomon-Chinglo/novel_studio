from typing import ClassVar

from pydantic import BaseModel, Field

from app.modules.base.schemas import MaterialCategory, MaterialMood


class ChapterSceneBeat(BaseModel):
    _prompt_labels: ClassVar[dict[str, str]] = {
        "category": "描写技法",
        "mood": "情绪",
        "description": "具体的剧情动作点",
    }

    category: MaterialCategory
    mood: MaterialMood
    description: str

    def prompt(self, index: int | None = None):
        data = self.model_dump(exclude_none=True)
        scene_beat = {self._prompt_labels.get(k, k): v for k, v in data.items()}
        content = "\n\n".join([f"- **{k}**: {v}" for k, v in scene_beat.items()])
        _index = f"{index}" if index else ""
        return f"<场景节拍{_index}>\n{content}\n</场景节拍{index}>"


class ChapterSceneBlueprint(BaseModel):
    _prompt_labels: ClassVar[dict[str, str]] = {
        "location": "场景地点",
        "time_setting": "场景时间及环境",
        "characters": "场景中的人物",
        "objective": "本场细的目标",
        "logic_bridge": "本场戏承接substory的哪一条",
    }

    location: str
    time_setting: str
    characters: list[str]
    objective: str
    logic_bridge: str

    def prompt(self, index: int | None = None):
        data = self.model_dump(exclude_none=True)
        scene_blueprint = {self._prompt_labels.get(k, k): v for k, v in data.items()}
        scene_blueprint["场景中的人物"] = ",".join(data["characters"])
        content = "\n\n".join([f"- **{k}**: {v}" for k, v in scene_blueprint.items()])
        _index = f"{index}" if index else ""
        return f"<场景蓝图{_index}>\n{content}\n</场景蓝图{_index}>"


class ChapterScene(ChapterSceneBlueprint):
    _prompt_labels: ClassVar[dict[str, str]] = {
        **ChapterSceneBlueprint._prompt_labels,
        "beats": "场景内的动作节拍序列",
    }

    beats: list[ChapterSceneBeat] = Field(min_length=1)

    def prompt(self, index: int | None = None):
        data = self.model_dump(exclude_none=True, exclude={"beats"})
        scene = {self._prompt_labels.get(k, k): v for k, v in data.items()}
        scene["场景中的人物"] = ",".join(data["characters"])
        scene_beats = "\n\n".join([beat.prompt(index + 1) for index, beat in enumerate(self.beats)])
        content = "\n\n".join([f"- **{k}**: {v}" for k, v in scene.items()])
        _index = f"{index}" if index else ""
        return f"<场景{_index}>\n{content}\n<场景节拍列表>\n{scene_beats}\n</场景节拍列表>\n</场景{_index}>"


class ChapterBase(BaseModel):
    _prompt_labels: ClassVar[dict[str, str]] = {
        "chapter_index": "章节序号",
        "title": "章节标题",
        "thematic_tone": "章节主题色调",
        "opening_hook": "章节开头的悬念",
        "ending_cliffhanger": "章节结尾的悬念",
    }

    chapter_index: int
    title: str
    thematic_tone: str
    opening_hook: str | None = None
    ending_cliffhanger: str | None = None


class ChapterBlueprint(ChapterBase):
    _prompt_labels: ClassVar[dict[str, str]] = {
        **ChapterBase._prompt_labels,
        "scenes_blueprint": "序列场景蓝图",
    }

    scenes_blueprint: list[ChapterSceneBlueprint] = Field(min_length=1)

    def prompt(self):
        data = self.model_dump(exclude_none=True, exclude={"scenes_blueprint"})
        chapter_blueprint = {self._prompt_labels.get(k, k): v for k, v in data.items()}
        scenes_blueprint = "\n\n".join(
            [
                scene_blueprint.prompt(index + 1)
                for index, scene_blueprint in enumerate(self.scenes_blueprint)
            ]
        )
        content = "\n\n".join([f"## {k}\n{v}" for k, v in chapter_blueprint.items()])
        return f"<章节蓝图>\n{content}\n<场景骨架列表>\n{scenes_blueprint}\n</场景骨架列表>\n</章节蓝图>"


class Chapter(ChapterBase):
    _prompt_labels: ClassVar[dict[str, str]] = {
        **ChapterBase._prompt_labels,
        "scenes": "章节内的场景序列",
    }

    scenes: list[ChapterScene] = Field(min_length=1)

    def prompt(self):
        data = self.model_dump(exclude_none=True, exclude={"scenes"})
        chapter = {self._prompt_labels.get(k, k): v for k, v in data.items()}
        scenes = "\n\n".join([scene.prompt(index + 1) for index, scene in enumerate(self.scenes)])
        content = "\n\n".join([f"## {k}\n{v}" for k, v in chapter.items()])
        return f"<章节>\n{content}\n<场景列表>\n{scenes}\n</场景列表>\n</章节>"
