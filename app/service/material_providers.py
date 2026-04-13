import asyncio
from collections.abc import Sequence
from dataclasses import dataclass

from app.modules.base import MaterialCategory, MaterialMood
from app.modules.materials import MaterialSnippet
from app.modules.outlines.schemas import ChapterScene, ChapterSceneBeat
from app.modules.writing import MaterialProvider
from app.service.materials import MaterialService

type SearchPlan = tuple[MaterialCategory | None, MaterialMood | None]


@dataclass(slots=True, frozen=True)
class HybridSearchPolicy:
    semantic_weight: float = 0.7
    lexical_weight: float = 0.3
    rrf_k: int = 60
    candidate_multiplier: int = 2
    min_candidate_limit: int = 4

    def __post_init__(self) -> None:
        if self.semantic_weight < 0:
            raise ValueError("semantic_weight must be non-negative.")
        if self.lexical_weight < 0:
            raise ValueError("lexical_weight must be non-negative.")
        if self.semantic_weight == 0 and self.lexical_weight == 0:
            raise ValueError("At least one search weight must be positive.")
        if self.rrf_k < 0:
            raise ValueError("rrf_k must be non-negative.")
        if self.candidate_multiplier < 1:
            raise ValueError("candidate_multiplier must be at least 1.")
        if self.min_candidate_limit < 1:
            raise ValueError("min_candidate_limit must be at least 1.")


class NoopMaterialProvider(MaterialProvider):
    async def provide_materials_for_scene(
        self, scene: ChapterScene, num_for_each_beat: int = 2
    ) -> list[MaterialSnippet]:
        return []


class HybridSearchMaterialProvider(MaterialProvider):
    def __init__(
        self,
        material_service: MaterialService | None = None,
        policy: HybridSearchPolicy | None = None,
    ) -> None:
        self.material_service = material_service or MaterialService()
        self.policy = policy or HybridSearchPolicy()

    def _dedupe_key(self, snippet: MaterialSnippet) -> str:
        return snippet.essential_text

    def _build_semantic_query(self, scene: ChapterScene, beat: ChapterSceneBeat) -> str:
        parts = [
            beat.description.strip(),
            scene.objective.strip(),
            scene.location.strip(),
            scene.logic_bridge.strip(),
        ]
        return "；".join(part for part in parts if part)

    def _build_lexical_query(self, beat: ChapterSceneBeat) -> str:
        return beat.description.strip()

    def _iter_search_plans(self, beat: ChapterSceneBeat) -> tuple[SearchPlan, ...]:
        return (
            (beat.category, beat.mood),
            (beat.category, None),
            (None, beat.mood),
            (None, None),
        )

    def _append_unique_until_limit(
        self,
        target: list[MaterialSnippet],
        seen: set[str],
        snippets: Sequence[MaterialSnippet],
        *,
        limit: int,
    ) -> bool:
        for snippet in snippets:
            key = self._dedupe_key(snippet)
            if key in seen:
                continue
            seen.add(key)
            target.append(snippet)
            if len(target) >= limit:
                return True
        return False

    def _candidate_limit(self, limit: int) -> int:
        return max(
            limit * self.policy.candidate_multiplier,
            self.policy.min_candidate_limit,
        )

    def _fuse_results(
        self,
        *,
        semantic_results: Sequence[MaterialSnippet],
        lexical_results: Sequence[MaterialSnippet],
        limit: int,
    ) -> list[MaterialSnippet]:
        scores: dict[str, float] = {}
        snippets: dict[str, MaterialSnippet] = {}

        for rank, snippet in enumerate(semantic_results, start=1):
            key = self._dedupe_key(snippet)
            snippets[key] = snippet
            scores[key] = scores.get(key, 0.0) + self.policy.semantic_weight / (
                self.policy.rrf_k + rank
            )

        for rank, snippet in enumerate(lexical_results, start=1):
            key = self._dedupe_key(snippet)
            snippets[key] = snippet
            scores[key] = scores.get(key, 0.0) + self.policy.lexical_weight / (
                self.policy.rrf_k + rank
            )

        ranked_keys = sorted(scores, key=lambda key: scores[key], reverse=True)
        return [snippets[key] for key in ranked_keys[:limit]]

    async def _search_for_beat(
        self,
        *,
        scene: ChapterScene,
        beat: ChapterSceneBeat,
        limit: int,
    ) -> list[MaterialSnippet]:
        if limit <= 0:
            return []

        semantic_query = self._build_semantic_query(scene, beat)
        lexical_query = self._build_lexical_query(beat)
        candidate_limit = self._candidate_limit(limit)

        collected: list[MaterialSnippet] = []
        seen: set[str] = set()

        for category, mood in self._iter_search_plans(beat):
            semantic_results, lexical_results = await asyncio.gather(
                self.material_service.search_semantic(
                    query=semantic_query,
                    limit=candidate_limit,
                    category=category,
                    mood=mood,
                ),
                self.material_service.search_lexical(
                    query=lexical_query,
                    limit=candidate_limit,
                    category=category,
                    mood=mood,
                ),
            )
            fused_results = self._fuse_results(
                semantic_results=semantic_results,
                lexical_results=lexical_results,
                limit=limit,
            )
            if self._append_unique_until_limit(collected, seen, fused_results, limit=limit):
                return collected

        return collected

    async def provide_materials_for_scene(
        self, scene: ChapterScene, num_for_each_beat: int = 2
    ) -> list[MaterialSnippet]:
        if num_for_each_beat <= 0 or not scene.beats:
            return []

        materials: list[MaterialSnippet] = []
        seen: set[str] = set()

        for beat in scene.beats:
            beat_materials = await self._search_for_beat(
                scene=scene,
                beat=beat,
                limit=num_for_each_beat,
            )
            self._append_unique_until_limit(
                materials, seen, beat_materials, limit=len(scene.beats) * num_for_each_beat
            )

        return materials
