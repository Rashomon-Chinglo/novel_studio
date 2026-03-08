from inline_snapshot import snapshot
from app.modules.writing.schemas import Chapter, SceneChunk
import pytest


@pytest.fixture
def scene_chunk_1() -> SceneChunk:
    return SceneChunk(content="李四深吸一口气，推开了沉重的铁门。")


@pytest.fixture
def scene_chunk_2() -> SceneChunk:
    return SceneChunk(content="进入铁门后，引入眼帘的是不可名状的怪物。")


@pytest.fixture
def chapter(scene_chunk_1: SceneChunk, scene_chunk_2: SceneChunk) -> Chapter:
    return Chapter(chunks=[scene_chunk_1, scene_chunk_2])


@pytest.mark.unit()
def test_scene_chunk_dump(
    scene_chunk_1: SceneChunk,
    scene_chunk_2: SceneChunk,
) -> None:
    assert scene_chunk_1.model_dump() == snapshot({"content": "李四深吸一口气，推开了沉重的铁门。"})
    assert scene_chunk_2.model_dump() == snapshot(
        {"content": "进入铁门后，引入眼帘的是不可名状的怪物。"}
    )


@pytest.mark.unit()
def test_scene_chunk_prompt(scene_chunk_1: SceneChunk, scene_chunk_2: SceneChunk) -> None:
    assert scene_chunk_1.prompt() == snapshot("李四深吸一口气，推开了沉重的铁门。")
    assert scene_chunk_2.prompt() == snapshot("进入铁门后，引入眼帘的是不可名状的怪物。")


@pytest.mark.unit()
def test_chapter_dump(chapter: Chapter) -> None:
    assert chapter.model_dump() == snapshot(
        {
            "chunks": [
                {"content": "李四深吸一口气，推开了沉重的铁门。"},
                {"content": "进入铁门后，引入眼帘的是不可名状的怪物。"},
            ]
        }
    )


@pytest.mark.unit()
def test_chapter_prompt(chapter: Chapter) -> None:
    assert chapter.prompt() == snapshot("""\
<章节正文>
李四深吸一口气，推开了沉重的铁门。
进入铁门后，引入眼帘的是不可名状的怪物。
</章节正文>\
""")
