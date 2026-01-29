import asyncio
import os
import sys

# Ensure app package is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.modules.outlines.context.bible import BibleBrainstormContext, BibleGenerateContext
    from app.modules.outlines.engines.bible import BibleEngine
except ImportError as e:
    print(f"Error importing BibleEngine: {e}")
    sys.exit(1)


async def main():
    print("🚀 [Auto] Bible Flow Complete Test")
    print("=" * 60)

    try:
        engine = BibleEngine()
        print("✅ BibleEngine initialized successfully")
    except Exception as e:
        print(f"❌ BibleEngine initialization failed: {e}")
        return

    # Simulated conversation history
    simulated_conversations = [
        ("我想写一个赛博朋克风格的侦探故事。", None),
        (
            None,
            "这是一个非常经典且充满潜力的题材。我们可以从主角的身份设定、案件的性质，以及赛博朋克世界独特的社会结构（例如高科技低生活、财团统治等）来切入。你希望主角是一个什么样的侦探？是传统的硬汉派，还是有什么特殊的赛博义体改造？",
        ),
        ("主角是一个拥有老式义眼的落魄侦探，案件涉及一个合成人偶像的谋杀。", None),
        (
            None,
            "老式义眼是一个很棒的细节，暗示主角可能经济拮据或是怀旧。合成人偶像的谋杀案也很有潜力，可以探讨人工智能的权利和尊严。你觉得这个案件背后的真相是什么？是简单的谋杀还是牵涉更大的阴谋？",
        ),
        ("案件背后是两大财团的权力斗争，偶像只是棋子。", None),
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
                context = BibleBrainstormContext(history=history, user_input=user_msg)
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
    print("Phase 2: Bible Generation")
    print("=" * 60)
    print(f"📊 Context: {len(history)} messages in history")

    # Generate Bible
    try:
        context = BibleGenerateContext(messages=history)
        bible = await engine.generate(context)

        print("\n🎉 " + "=" * 50 + " 🎉")
        print("         [STORY BIBLE GENERATED]")
        print("=" * 56)
        print(f"📖 Title: 《{bible.title}》")
        print(f"📝 Logline: {bible.logline}")
        print("-" * 56)
        print(f"🔥 Marketing Hook:\n   {bible.marketing_hook}")
        print("-" * 56)
        print(f"🌍 Worldview Tone:\n   {bible.worldview_tone}")
        print("-" * 56)
        print(f"⚔️ Main Conflict:\n   {bible.main_conflict}")
        print("-" * 56)
        print(f"🏁 Ending Vision:\n   {bible.ending_vision}")
        print("-" * 56)
        print(f"👥 Key Roles:\n   {bible.key_roles_summary}")
        print("=" * 56)

        print("\n✅ Bible flow test completed successfully!")

    except Exception as e:
        print(f"\n❌ Bible generation failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
