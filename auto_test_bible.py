import asyncio
import sys
import os

# Ensure app package is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.modules.outlines.engines.bible import BibleEngine
except ImportError as e:
    print(f"Error importing BibleEngine: {e}")
    sys.exit(1)


async def main():
    print("🚀 [Auto] Bible Flow Automation")

    history = [
        "User: 我想写一个赛博朋克风格的侦探故事。",
        "AI: 这是一个非常经典且充满潜力的题材。我们可以从主角的身份设定、案件的性质，以及赛博朋克世界独特的社会结构（例如高科技低生活、财团统治等）来切入。你希望主角是一个什么样的侦探？是传统的硬汉派，还是有什么特殊的赛博义体改造？",
        "User: 主角是一个拥有老式义眼的落魄侦探，案件涉及一个合成人偶像的谋杀。",
    ]

    try:
        engine = BibleEngine()
    except Exception as e:
        print(f"❌ BibleEngine Initialization Failed: {e}")
        return

    for i in range(1, 11):
        print(f"\n--- Iteration {i}/10 ---")
        try:
            bible = await engine.generate(history)
            print(f"Object: {bible}")

            # Print Key-Values
            print(bible.model_dump())

        except Exception as e:
            print(f"❌ Iteration {i} Failed: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
