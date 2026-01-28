from pydantic import BaseModel, Field


class SceneBeat(BaseModel):
    type: str = Field(alias="场景类型")
    description: str = Field(alias="具体的剧情动作点")

    def prompt(self, index: int | None = None):
        scene_beat = self.model_dump(exclude_none=True, by_alias=True)
        content = "\n\n".join([f"- **{k}**: {v}" for k, v in scene_beat.items()])
        index = f"{index}" if index else ""
        return f"<场景节拍{index}>\n{content}\n</场景节拍{index}>"


class SceneBlueprint(BaseModel):
    location: str = Field(alias="场景地点")
    time_setting: str = Field(alias="场景时间及环境")
    characters: list[str] = Field(alias="场景中的人物")
    objective: str = Field(alias="本场细的目标")
    logic_bridge: str = Field(alias="本场戏承接substory的哪一条")

    def prompt(self, index: int | None = None):
        scene_blueprint = self.model_dump(exclude_none=True, by_alias=True)
        scene_blueprint["场景中的人物"] = ",".join(scene_blueprint["场景中的人物"])
        content = "\n\n".join([f"- **{k}**: {v}" for k, v in scene_blueprint.items()])
        index = f"{index}" if index else ""
        return f"<场景蓝图{index}>\n{content}\n</场景蓝图{index}>"


class Scene(SceneBlueprint):
    beats: list[SceneBeat] = Field(alias="场景内的动作节拍序列", min_length=1)

    def prompt(self, index: int | None = None):
        scene = self.model_dump(exclude_none=True, by_alias=True, exclude={"beats"})
        scene["场景中的人物"] = ",".join(scene["场景中的人物"])
        scene_beats = "\n\n".join(
            [beat.prompt(index + 1) for index, beat in enumerate(self.beats)]
        )
        content = "\n\n".join([f"- **{k}**: {v}" for k, v in scene.items()])
        index = f"{index}" if index else ""
        return f"<场景{index}>\n{content}\n<场景节拍列表>\n{scene_beats}\n</场景节拍列表>\n</场景{index}>"


class ChapterBase(BaseModel):
    chapter_index: int = Field(alias="章节序号")
    title: str = Field(alias="章节标题")
    thematic_tone: str = Field(alias="章节主题色调")
    opening_hook: str | None = Field(alias="章节开头的悬念")
    ending_cliffhanger: str | None = Field(alias="章节结尾的悬念")


class ChapterBlueprint(ChapterBase):
    scenes_blueprint: list[SceneBlueprint] = Field(alias="序列场景蓝图", min_length=1)

    def prompt(self):
        chapter_blueprint = self.model_dump(
            exclude_none=True, by_alias=True, exclude={"scenes_blueprint"}
        )
        scenes_blueprint = "\n\n".join(
            [
                scene_blueprint.prompt(index + 1)
                for index, scene_blueprint in enumerate(self.scenes_blueprint)
            ]
        )
        content = "\n\n".join([f"## {k}\n{v}" for k, v in chapter_blueprint.items()])
        return f"<章节蓝图>\n{content}\n<场景骨架列表>\n{scenes_blueprint}\n</场景骨架列表>\n</章节蓝图>"


class Chapter(ChapterBase):
    scenes: list[Scene] = Field(alias="章节内的场景序列", min_length=1)

    def prompt(self):
        chapter = self.model_dump(exclude_none=True, by_alias=True, exclude={"scenes"})
        scenes = "\n\n".join(
            [scene.prompt(index + 1) for index, scene in enumerate(self.scenes)]
        )
        content = "\n\n".join([f"## {k}\n{v}" for k, v in chapter.items()])
        return f"<章节>\n{content}\n<场景列表>\n{scenes}\n</场景列表>\n</章节>"
