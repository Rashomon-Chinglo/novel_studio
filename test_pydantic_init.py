from app.modules.outlines.schemas.chapter import Chapter, ChapterScene, ChapterSceneBeat


def test_chapter_init():
    try:
        beat = ChapterSceneBeat(type="对话", description="两人交谈")
        scene = ChapterScene(
            location="客厅",
            time_setting="晚上",
            characters=["张三", "李四"],
            objective="弄清真相",
            logic_bridge="承接上文",
            beats=[beat],
        )
        chapter = Chapter(
            chapter_index=1,
            title="第一章",
            thematic_tone="压抑",
            opening_hook="悬念",
            ending_cliffhanger="断点",
            scenes=[scene],
        )
        print("✅ Chapter initialized successfully!")

        # 测试 prompt 输出
        print("\n--- ChapterSceneBeat prompt ---")
        print(beat.prompt(1))

        print("\n--- ChapterScene prompt ---")
        print(scene.prompt(1))

        print("\n--- Chapter prompt ---")
        print(chapter.prompt())

    except Exception as e:
        print(f"❌ Failed to initialize Chapter: {e}")


if __name__ == "__main__":
    test_chapter_init()
