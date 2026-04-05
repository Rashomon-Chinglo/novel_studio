from .chain import get_scene_writing_chain
from .context import ChapterSceneWritingContext, ChapterWritingContext
from .prompt import ChapterSceneWritingPrompt
from .providers import MaterialProvider
from .schemas import SceneChunk, WrittenChapter


class WritingEngine:
    ChapterSceneWritingContext = ChapterSceneWritingContext
    ChapterWritingContext = ChapterWritingContext

    def __init__(self, material_provider: MaterialProvider):
        self.material_provider = material_provider
        self.chunk_template = ChapterSceneWritingPrompt()
        self.scene_llm = get_scene_writing_chain(self.chunk_template.prompt)

    async def scene_writing(self, context: ChapterSceneWritingContext) -> SceneChunk:
        variables = self.chunk_template.build_variables(context)
        result = await self.scene_llm.ainvoke(variables)
        return SceneChunk(content=result)

    async def writing(self, context: ChapterWritingContext) -> WrittenChapter:
        scene_chunks: list[SceneChunk] = []
        for scene_blueprint, scene in zip(
            context.chapter_blueprint.scenes_blueprint, context.chapter_outline.scenes, strict=True
        ):
            scene_context = self.ChapterSceneWritingContext(
                bible=context.bible,
                substory=context.substory,
                original_logic_nodes=context.original_logic_nodes,
                chapter_blueprint=context.chapter_blueprint,
                scene_blueprint=scene_blueprint,
                scene=scene,
                cumulative_substory_summary=context.cumulative_substory_summary,
                pre_chapter_summary=context.pre_chapter_summary,
                previous_scene_chunk=scene_chunks[-1]
                if scene_chunks
                else context.previous_scene_chunk,
                materials=await self.material_provider.provide_materials_for_scene(scene=scene),
            )
            scene_chunk = await self.scene_writing(scene_context)
            scene_chunks.append(scene_chunk)

        return WrittenChapter(chunks=scene_chunks)
