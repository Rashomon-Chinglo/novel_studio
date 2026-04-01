from typing import Protocol

from app.modules.materials import MaterialSnippet
from app.modules.outlines.schemas import ChapterScene


class MaterialProvider(Protocol):
    async def provide_materials_for_scene(
        self, scene: ChapterScene, num_for_each_beat: int = 2
    ) -> list[MaterialSnippet]:
        """
        Provide materials for each beat in the scene.
        """
        ...
