import pytest
from inline_snapshot import snapshot

from app.modules.outlines.schemas.chapter import (
    ChapterBlueprint,
    ChapterOutline,
    ChapterScene,
    ChapterSceneBeat,
    ChapterSceneBlueprint,
)


@pytest.fixture()
def scene_beat() -> ChapterSceneBeat:
    return ChapterSceneBeat(
        category="动作",
        mood="激昂",
        description="李四翻滚躲开射击，同时抛出一枚自制电磁脉冲手雷",
    )


@pytest.fixture()
def scene_blueprint() -> ChapterSceneBlueprint:
    return ChapterSceneBlueprint(
        location="贫民窟的废弃工厂巷道",
        time_setting="深夜，暴雨倾盆",
        characters=["李四", "黑帮小喽啰", "妹妹小红"],
        objective="李四试图带着妹妹逃离黑帮的包围圈",
        logic_bridge="承接卷一节点1：黑帮火拼爆发",
    )


@pytest.fixture()
def scene(scene_blueprint: ChapterSceneBlueprint, scene_beat: ChapterSceneBeat) -> ChapterScene:
    return ChapterScene(
        **scene_blueprint.model_dump(),
        beats=[scene_beat],
    )


@pytest.fixture()
def chapter_blueprint(scene_blueprint: ChapterSceneBlueprint) -> ChapterBlueprint:
    return ChapterBlueprint(
        chapter_index=1,
        substory_chapter_index=1,
        title="雨夜的枪声",
        thematic_tone="紧张、压抑",
        opening_hook="一颗子弹擦过李四的耳边，打碎了身后的净水器",
        ending_cliffhanger="李四倒在血泊中，眼看黑帮老大举起了枪，突然他的手心闪烁起蓝色的电光……",
        scenes_blueprint=[scene_blueprint],
    )


@pytest.fixture()
def chapter_outline(scene: ChapterScene) -> ChapterOutline:
    return ChapterOutline(
        chapter_index=1,
        substory_chapter_index=1,
        title="雨夜的枪声",
        thematic_tone="紧张、压抑",
        opening_hook="一颗子弹擦过李四的耳边，打碎了身后的净水器",
        ending_cliffhanger="李四倒在血泊中，眼看黑帮老大举起了枪，突然他的手心闪烁起蓝色的电光……",
        scenes=[scene],
    )


@pytest.mark.unit()
def test_chapter_scene_beat_prompt(scene_beat: ChapterSceneBeat) -> None:
    assert scene_beat.prompt(index=1) == snapshot("""\
<场景节拍1>
- **描写技法**: 动作

- **情绪**: 激昂

- **具体的剧情动作点**: 李四翻滚躲开射击，同时抛出一枚自制电磁脉冲手雷
</场景节拍1>\
""")


@pytest.mark.unit()
def test_chapter_scene_blueprint_prompt(scene_blueprint: ChapterSceneBlueprint) -> None:
    assert scene_blueprint.prompt(index=1) == snapshot("""\
<场景蓝图1>
- **场景地点**: 贫民窟的废弃工厂巷道

- **场景时间及环境**: 深夜，暴雨倾盆

- **场景中的人物**: 李四,黑帮小喽啰,妹妹小红

- **本场细的目标**: 李四试图带着妹妹逃离黑帮的包围圈

- **本场戏承接substory的哪一条**: 承接卷一节点1：黑帮火拼爆发
</场景蓝图1>\
""")


@pytest.mark.unit()
def test_chapter_scene_prompt(scene: ChapterScene) -> None:
    assert scene.prompt(index=1) == snapshot("""\
<场景1>
- **场景地点**: 贫民窟的废弃工厂巷道

- **场景时间及环境**: 深夜，暴雨倾盆

- **场景中的人物**: 李四,黑帮小喽啰,妹妹小红

- **本场细的目标**: 李四试图带着妹妹逃离黑帮的包围圈

- **本场戏承接substory的哪一条**: 承接卷一节点1：黑帮火拼爆发
<场景节拍列表>
<场景节拍1>
- **描写技法**: 动作

- **情绪**: 激昂

- **具体的剧情动作点**: 李四翻滚躲开射击，同时抛出一枚自制电磁脉冲手雷
</场景节拍1>
</场景节拍列表>
</场景1>\
""")


@pytest.mark.unit()
def test_chapter_blueprint_prompt(chapter_blueprint: ChapterBlueprint) -> None:
    assert chapter_blueprint.prompt() == snapshot("""\
<章节蓝图>
## 章节序号
1

## substory内章节序号
1

## 章节标题
雨夜的枪声

## 章节主题色调
紧张、压抑

## 章节开头的悬念
一颗子弹擦过李四的耳边，打碎了身后的净水器

## 章节结尾的悬念
李四倒在血泊中，眼看黑帮老大举起了枪，突然他的手心闪烁起蓝色的电光……
<场景骨架列表>
<场景蓝图1>
- **场景地点**: 贫民窟的废弃工厂巷道

- **场景时间及环境**: 深夜，暴雨倾盆

- **场景中的人物**: 李四,黑帮小喽啰,妹妹小红

- **本场细的目标**: 李四试图带着妹妹逃离黑帮的包围圈

- **本场戏承接substory的哪一条**: 承接卷一节点1：黑帮火拼爆发
</场景蓝图1>
</场景骨架列表>
</章节蓝图>\
""")


@pytest.mark.unit()
def test_chapter_prompt(chapter_outline: ChapterOutline) -> None:
    assert chapter_outline.prompt() == snapshot("""\
<章节>
## 章节序号
1

## substory内章节序号
1

## 章节标题
雨夜的枪声

## 章节主题色调
紧张、压抑

## 章节开头的悬念
一颗子弹擦过李四的耳边，打碎了身后的净水器

## 章节结尾的悬念
李四倒在血泊中，眼看黑帮老大举起了枪，突然他的手心闪烁起蓝色的电光……
<场景列表>
<场景1>
- **场景地点**: 贫民窟的废弃工厂巷道

- **场景时间及环境**: 深夜，暴雨倾盆

- **场景中的人物**: 李四,黑帮小喽啰,妹妹小红

- **本场细的目标**: 李四试图带着妹妹逃离黑帮的包围圈

- **本场戏承接substory的哪一条**: 承接卷一节点1：黑帮火拼爆发
<场景节拍列表>
<场景节拍1>
- **描写技法**: 动作

- **情绪**: 激昂

- **具体的剧情动作点**: 李四翻滚躲开射击，同时抛出一枚自制电磁脉冲手雷
</场景节拍1>
</场景节拍列表>
</场景1>
</场景列表>
</章节>\
""")
