import asyncio
import os
import sys

# Ensure app package is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.modules.outlines.context.bible import BibleBrainstormContext, BibleGenerateContext
    from app.modules.outlines.context.substory import (
        SubstoryBrainstormContext,
        SubstoryGenerateContext,
    )
    from app.modules.outlines.engines.bible import BibleEngine
    from app.modules.outlines.engines.substory import SubstoryEngine
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)


async def run_bible_phase():
    """Phase 1: Automated Bible Generation"""
    print("\n🚀 [PHASE 1] Story Bible Generation")
    print("=" * 60)

    engine = BibleEngine()

    # Simulated Bible brainstorm conversation
    bible_conversations = [
        ("我想写一本修仙题材的小说，主角是个废柴逆袭。", None),
        (
            None,
            "修仙废柴流是经典设定！我们要思考几个问题：主角为什么是废柴？金手指是什么？核心爽点在哪？你有什么想法？",
        ),
        ("主角天生经脉堵塞，但意外得到上古传承。", None),
        (
            None,
            "上古传承是很好的金手指！那这个传承有什么特殊之处？比如修炼功法、法宝、还是特殊能力？",
        ),
        ("传承包含逆天功法，可以重塑经脉，还有炼丹术。", None),
    ]

    history = []
    print("Simulating brainstorm conversations...")

    for user_msg, ai_msg in bible_conversations:
        if user_msg:
            context = BibleBrainstormContext(history=history, user_input=user_msg)
            response = await engine.brainstorm(context)
            history.append(f"User: {user_msg}")
            history.append(f"AI: {response}")
        elif ai_msg:
            history.append(f"AI: {ai_msg}")

    print(f"✅ Brainstorm completed with {len(history)} messages")

    # Generate Bible
    print("\n⚙️ Generating Story Bible...")
    context = BibleGenerateContext(messages=history)
    bible = await engine.generate(context)

    print("\n🎉 " + "=" * 50 + " 🎉")
    print("         [STORY BIBLE GENERATED]")
    print("=" * 56)
    print(f"📖 Title: 《{bible.title}》")
    print(f"📝 Logline: {bible.logline}")
    print(f"🌍 Tone: {bible.worldview_tone}")
    print("=" * 56)

    return bible, history


async def run_substory_phase(bible):
    """Phase 2: Automated Substory Generation"""
    print("\n\n🚀 [PHASE 2] Substory (Volume/Arc) Generation")
    print("=" * 60)
    print(f"📚 Based on Bible: 《{bible.title}》")
    print("=" * 60)

    engine = SubstoryEngine()

    # Simulated Substory brainstorm conversation
    substory_conversations = [
        ("第一卷讲主角在宗门受尽欺凌，最后觉醒传承。", None),
        (
            None,
            "好的开局！欺凌可以塑造读者的代入感。那具体的触发事件是什么？比如生死危机、羞辱到极点等？",
        ),
        ("在一次生死试炼中被同门暗算，命悬一线时觉醒。", None),
        (
            None,
            "生死关头觉醒是很燃的爆点！那觉醒后的第一个爽点是什么？直接复仇还是先隐藏实力？",
        ),
        ("先隐藏实力，暗中修炼，然后在宗门大比上一鸣惊人。", None),
    ]

    history = []
    print("Simulating brainstorm conversations...")

    for user_msg, ai_msg in substory_conversations:
        if user_msg:
            context = SubstoryBrainstormContext(history=history, user_input=user_msg, bible=bible)
            response = await engine.brainstorm(context)
            history.append(f"User: {user_msg}")
            history.append(f"AI: {response}")
        elif ai_msg:
            history.append(f"AI: {ai_msg}")

    print(f"✅ Brainstorm completed with {len(history)} messages")

    # Generate Substory
    print("\n⚙️ Generating Substory Outline...")
    context = SubstoryGenerateContext(history=history, bible=bible)
    substory = await engine.generate(context)

    print("\n🎉 " + "=" * 50 + " 🎉")
    print("      [SUBSTORY OUTLINE GENERATED]")
    print("=" * 56)
    print(f"📑 Title: {substory.substory_title}")
    print(f"🔥 Core Conflict: {substory.core_conflict}")
    print(f"🔄 Status Change: {substory.status_change}")
    print("-" * 56)
    print("🔗 Logic Chain:")
    for i, node in enumerate(substory.logic_nodes, 1):
        print(f"  {i}. [Cause] {node.cause}")
        print(f"     -> [Process] {node.process}")
        print(f"     -> [Effect] {node.effect}")
        print(f"     (Exchange: {node.exchange})")
        print()
    print("=" * 56)


async def main():
    print("\n🌟 " + "=" * 54 + " 🌟")
    print("     [AUTO] COMPLETE STORY FLOW TEST")
    print("     Bible → Substory → Full Pipeline")
    print("=" * 60 + "\n")

    try:
        # Phase 1: Bible
        result = await run_bible_phase()
        if not result:
            print("❌ Bible phase failed")
            return

        bible, _ = result

        # Phase 2: Substory
        await run_substory_phase(bible)

        print("\n✅ Complete story flow test finished successfully!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
