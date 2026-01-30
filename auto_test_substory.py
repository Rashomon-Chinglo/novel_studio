import asyncio
import os
import sys

# Ensure app package is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.modules.outlines.engines.substory import SubstoryEngine
    from app.modules.outlines.schemas.bible import Bible
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)

DUMMY_BIBLE = Bible(
    title="迷雾都市：赛博侦探",
    logline="在2077年的霓虹废墟中，一名拥有老式义眼的落魄侦探必须在三天内破解合成人偶像的谋杀案，否则将引爆两大财团的核战争。",
    marketing_hook="硬核侦探推理 + 赛博朋克暴力美学，反转不断的悬疑剧情。",
    worldview_tone="赛博朋克，黑色电影，压抑，高科技低生活",
    main_conflict="底层侦探 vs 掌控城市的超级财团",
    ending_vision="侦探揭露了真相，却发现自己也是被操控的一枚棋子，最终选择自我毁灭以换取城市的自由。",
    key_roles_summary="雷蒙德（主角）：老练、愤世嫉俗的私家侦探。艾娃（配角）：具有自我意识的实验型AI，拥有骇入一切的能力。",
)


async def main():
    print("🚀 [Auto] Substory Flow Automation")

    history = [
        "User: 第一卷讲主角接到案子，去调查现场，发现被财团监视。",
        "AI: 好的，这是一个很好的开端。我们可以安排主角在调查过程中发现一些不该发现的线索，从而引来财团的杀手。你觉得具体的线索是什么？",
        "User: 线索是偶像体内的一个加密芯片。",
    ]

    try:
        engine = SubstoryEngine()
    except Exception as e:
        print(f"❌ SubstoryEngine Initialization Failed: {e}")
        return

    for i in range(1, 2):
        print(f"\n--- Single Test Iteration {i}/1 ---")
        try:
            context = engine.SubstoryGenerateContext(history=history, bible=DUMMY_BIBLE)
            substory = await engine.generate(context)
            print(f"Object: {substory}")

            # Print Key-Values
            print(substory.model_dump())

        except Exception as e:
            print(f"❌ Iteration {i} Failed: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
