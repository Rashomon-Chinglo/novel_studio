import asyncio
import sys
import os
import readline  # Enable proper line editing (backspace, arrows)

# 1. Path fix to ensure app package is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.modules.outlines.engines.bible import BibleEngine
    from app.modules.outlines.engines.substory import SubstoryEngine
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Please run this script from the project root or ensure python path is correct.")
    sys.exit(1)


async def run_bible_phase():
    print("\n🚀 [PHASE 1] Story Bible Generation")
    print("---------------------------------------------------------")
    print("💡 Guide: Chat to brainstorm the main story idea.")
    print("   Type 'GEN' to finish brainstorming and generate the Bible.")
    print("---------------------------------------------------------")

    engine = BibleEngine()
    history = []

    while True:
        try:
            user_input = input("\n👤 User (Bible): ").strip()
        except EOFError:
            return None

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting...")
            sys.exit(0)

        # Trigger Generation
        if user_input.upper() == "GEN" or user_input == "生成":
            print("\n⚙️  [System] Generating Story Bible...")
            try:
                bible = await engine.generate(history)
                print("\n🎉 ============ [STORY BIBLE] ============ 🎉")
                print(f"📖 Title: {bible.title}")
                print(f"📝 Logline: {bible.logline}")
                print(f"🌍 Tone: {bible.worldview_tone}")
                print("===========================================")
                return bible, history  # Return bible and the history used
            except Exception as e:
                print(f"❌ Bible Generation Failed: {e}")
                import traceback
                traceback.print_exc()
                return None

        # Chat
        print("🤖 AI (Thinking)...", end="\r")
        try:
            response = await engine.brainstorm(history, user_input)
            print(" " * 20, end="\r")
            print(f"🤖 AI: {response}")
            
            # Append to history
            history.append(f"User: {user_input}")
            history.append(f"AI: {response}")

        except Exception as e:
            print(f"\n❌ Error: {e}")


async def run_substory_phase(bible):
    print("\n\n🚀 [PHASE 2] Substory (Volume/Arc) Generation")
    print("---------------------------------------------------------")
    print("💡 Guide: Now brainstorm the first volume/arc based on the Bible.")
    print("   Type 'GEN' to generate the Substory Outline.")
    print("---------------------------------------------------------")

    engine = SubstoryEngine(bible)
    history = []

    while True:
        try:
            user_input = input("\n👤 User (Substory): ").strip()
        except EOFError:
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting...")
            sys.exit(0)

        # Trigger Generation
        if user_input.upper() == "GEN" or user_input == "生成":
            print("\n⚙️  [System] Generating Substory Outline...")
            try:
                substory = await engine.generate(history)
                print("\n🎉 ============ [SUBSTORY OUTLINE] ============ 🎉")
                print(f"📑 Title: {substory.title}")
                print(f"🔥 Core Conflict: {substory.core_conflict}")
                print(f"🔄 Status Change: {substory.status_change}")
                print("-" * 50)
                print("🔗 Logic Chain (Nodes):")
                for i, node in enumerate(substory.logic_nodes, 1):
                    print(f"  {i}. [Cause] {node.cause}")
                    print(f"     -> [Process] {node.process}")
                    print(f"     -> [Effect] {node.effect}")
                    print(f"     (Exchange: {node.exchange})")
                    print()
                print("===============================================")
                break
            except Exception as e:
                print(f"❌ Substory Generation Failed: {e}")
                import traceback
                traceback.print_exc()
                break

        # Chat
        print("🤖 AI (Thinking)...", end="\r")
        try:
            response = await engine.brainstorm(history, user_input)
            print(" " * 20, end="\r")
            print(f"🤖 AI: {response}")

            # Append to history
            history.append(f"User: {user_input}")
            history.append(f"AI: {response}")

        except Exception as e:
            print(f"\n❌ Error: {e}")


async def main():
    # Phase 1: Bible
    result = await run_bible_phase()
    if not result:
        print("❌ Bible phase failed or aborted.")
        return
    
    bible, _ = result

    # Phase 2: Substory
    await run_substory_phase(bible)


if __name__ == "__main__":
    asyncio.run(main())
