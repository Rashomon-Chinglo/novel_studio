import pytest
from inline_snapshot import snapshot
from app.modules.outlines.schemas.bible import Bible


@pytest.fixture()
def bible() -> Bible:
    return Bible(
        title="测试小说名",
        logline="这是一个测试用的核心梗概，描述了主角的冒险故事。",
        marketing_hook="无敌流，快节奏，系统文",
        worldview_tone="赛博朋克风格废土世界，基调灰暗但充满希望",
        main_conflict="底层平民与财阀高层的生存资源争夺战",
        ending_vision="主角推翻财阀，建立新的秩序",
        key_roles_summary="主角李四是孤儿，配角王五是他的黑客导师",
    )


@pytest.mark.unit()
def test_bible_prompt(bible: Bible) -> None:
    assert bible.prompt() == snapshot("""\
<小说总纲>
## 书名
测试小说名

## 梗概
这是一个测试用的核心梗概，描述了主角的冒险故事。

## 核心卖点，爽点
无敌流，快节奏，系统文

## 世界观基调
赛博朋克风格废土世界，基调灰暗但充满希望

## 主线冲突
底层平民与财阀高层的生存资源争夺战

## 结局愿景
主角推翻财阀，建立新的秩序

## 主角们的简要概述
主角李四是孤儿，配角王五是他的黑客导师
</小说总纲>\
""")


@pytest.mark.unit()
def test_bible_prompt_exclude(bible: Bible) -> None:
    assert bible.prompt(exclude={"title", "logline"}) == snapshot("""\
<小说总纲>
## 核心卖点，爽点
无敌流，快节奏，系统文

## 世界观基调
赛博朋克风格废土世界，基调灰暗但充满希望

## 主线冲突
底层平民与财阀高层的生存资源争夺战

## 结局愿景
主角推翻财阀，建立新的秩序

## 主角们的简要概述
主角李四是孤儿，配角王五是他的黑客导师
</小说总纲>\
""")
