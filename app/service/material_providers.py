from app.modules.materials import MaterialSnippet
from app.modules.outlines.schemas import ChapterScene
from app.modules.writing import MaterialProvider


class NoopMaterialProvider(MaterialProvider):
    async def provide_materials_for_scene(
        self, scene: ChapterScene, num_for_each_beat: int = 2
    ) -> list[MaterialSnippet]:
        return []


class VectorSearchMaterialProvider(MaterialProvider):
    async def provide_materials_for_scene(
        self, scene: ChapterScene, num_for_each_beat: int = 2
    ) -> list[MaterialSnippet]:
        return []
