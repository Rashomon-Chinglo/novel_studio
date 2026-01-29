from ..chain.chapter import (
    get_chapter_blueprint_chain,
    get_chapter_brainstorm_chain,
    get_chapter_scene_chain,
)
from ..context.chapter import (
    ChapterBlueprintBrainstormContext,
    ChapterBlueprintContext,
    ChapterContext,
    ChapterSceneContext,
)
from ..prompts.chapter import (
    ChapterBlueprintBrainstormPrompt,
    ChapterBlueprintPrompt,
    ChapterScenePrompt,
)
from ..schemas.chapter import Chapter, ChapterBlueprint, ChapterScene


class ChapterEngine:
    ChapterBlueprintContext = ChapterBlueprintContext
    ChapterBlueprintBrainstormContext = ChapterBlueprintBrainstormContext
    ChapterSceneContext = ChapterSceneContext
    ChapterContext = ChapterContext

    def __init__(self):
        self.chapter_blueprint_brainstorm_template = ChapterBlueprintBrainstormPrompt()
        self.chapter_blueprint_template = ChapterBlueprintPrompt()
        self.chapter_scene_template = ChapterScenePrompt()

        self.brainstorm_llm = get_chapter_brainstorm_chain(
            self.chapter_blueprint_brainstorm_template.prompt
        )
        self.blueprint_llm = get_chapter_blueprint_chain(self.chapter_blueprint_template.prompt)
        self.chapter_llm = get_chapter_scene_chain(self.chapter_scene_template.prompt)

    async def chapter_blueprint_init(self, context: ChapterBlueprintContext) -> ChapterBlueprint:
        variables = self.chapter_blueprint_template.build_variables(context)
        result = await self.blueprint_llm.ainvoke(variables)
        return result

    async def chapter_blueprint_brainstorm(self, context: ChapterBlueprintBrainstormContext) -> str:
        variables = self.chapter_blueprint_brainstorm_template.build_variables(context)
        result = await self.brainstorm_llm.ainvoke(variables)
        return result

    async def chapter_blueprint_generate(
        self, context: ChapterBlueprintContext
    ) -> ChapterBlueprint:
        variables = self.chapter_blueprint_template.build_variables(context)
        result = await self.blueprint_llm.ainvoke(variables)
        return result

    async def chapter_scene_generate(self, context: ChapterSceneContext) -> ChapterScene:
        variables = self.chapter_scene_template.build_variables(context)
        result = await self.chapter_llm.ainvoke(variables)
        return result

    async def chapter_generate(self, context: ChapterContext) -> Chapter:
        scenes_blueprint = context.chapter_blueprint.scenes_blueprint
        scenes = []
        for scene_blueprint in scenes_blueprint:
            scene = await self.chapter_scene_generate(
                ChapterSceneContext(
                    last_scene_beat=scenes[-1].beats[-1] if scenes else None,
                    bible=context.bible,
                    substory=context.substory,
                    cumulative_substory_summary=context.cumulative_substory_summary,
                    pre_chapter_summary=context.pre_chapter_summary,
                    logic_nodes_to_process=context.logic_nodes_to_process,
                    chapter_blueprint=context.chapter_blueprint,
                    scene_blueprint=scene_blueprint,
                )
            )
            scenes.append(scene)
        return Chapter(
            chapter_index=context.chapter_blueprint.chapter_index,
            title=context.chapter_blueprint.title,
            thematic_tone=context.chapter_blueprint.thematic_tone,
            opening_hook=context.chapter_blueprint.opening_hook,
            ending_cliffhanger=context.chapter_blueprint.ending_cliffhanger,
            scenes=scenes,
        )
