import asyncio
import os
import sys

# Ensure app package is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.modules.outlines.context.substory import (
        SubstoryBrainstormContext,
        SubstoryGenerateContext,
    )
    from app.modules.outlines.engines.substory import SubstoryEngine
    from app.modules.outlines.schemas.bible import Bible
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)


# Dummy Bible for testing
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
    print("🚀 [Auto] Substory Flow Complete Test")
    print("=" * 60)
    print(f"📚 Based on Bible: 《{DUMMY_BIBLE.title}》")
    print("=" * 60)

    try:
        engine = SubstoryEngine()
        print("✅ SubstoryEngine initialized successfully")
    except Exception as e:
        print(f"❌ SubstoryEngine initialization failed: {e}")
        return

    # Simulated conversation history
    simulated_conversations = [
        ("第一卷讲主角接到案子，去调查现场，发现被财团监视。", None),
        (
            None,
            "好的，这是一个很好的开端。我们可以安排主角在调查过程中发现一些不该发现的线索，从而引来财团的杀手。你觉得具体的线索是什么？",
        ),
        ("线索是偶像体内的一个加密芯片，记录了财团的黑暗交易。", None),
        (
            None,
            "加密芯片是个很好的物证！那主角如何获得这个芯片？是在尸检时发现，还是有其他途径？另外，主角发现这个线索后会面临什么困境？",
        ),
        ("在非法尸检时发现，随后遭到追杀，不得不逃亡。", None),
    ]

    history = []

    print("\n" + "=" * 60)
    print("Phase 1: Brainstorm Simulation")
    print("=" * 60)

    # Simulate brainstorming process
    for i, (user_msg, ai_msg) in enumerate(simulated_conversations):
        if user_msg:
            print(f"\n👤 User: {user_msg}")
            try:
                context = SubstoryBrainstormContext(
                    history=history, user_input=user_msg, bible=DUMMY_BIBLE
                )
                response = await engine.brainstorm(context)
                print(f"🤖 AI: {response}")

                history.append(f"User: {user_msg}")
                history.append(f"AI: {response}")
            except Exception as e:
                print(f"❌ Brainstorm failed at step {i}: {e}")
                import traceback

                traceback.print_exc()
                return
        elif ai_msg:
            # Use pre-defined AI response for testing
            history.append(f"AI: {ai_msg}")

    print("\n" + "=" * 60)
    print("Phase 2: Substory Generation")
    print("=" * 60)
    print(f"📊 Context: {len(history)} messages in history")

    # Generate Substory
    try:
        context = SubstoryGenerateContext(history=history, bible=DUMMY_BIBLE)
        substory = await engine.generate(context)

        print("\n🎉 " + "=" * 50 + " 🎉")
        print("      [SUBSTORY OUTLINE GENERATED]")
        print("=" * 56)
        print(f"📑 Title: {substory.substory_title}")
        print(f"🔥 Core Conflict: {substory.core_conflict}")
        print(f"🔄 Status Change: {substory.status_change}")
        print("-" * 56)
        print("🔗 Logic Chain (Action Nodes):")
        for i, node in enumerate(substory.logic_nodes, 1):
            print(f"\n  [{i}]")
            print(f"  Cause   : {node.cause}")
            print(f"  Process : {node.process}")
            print(f"  Effect  : {node.effect}")
            print(f"  Exchange: {node.exchange}")
            if node.context:
                print(f"  Context : {node.context}")
        print("=" * 56)

        print("\n✅ Substory flow test completed successfully!")

    except Exception as e:
        print(f"\n❌ Substory generation failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
