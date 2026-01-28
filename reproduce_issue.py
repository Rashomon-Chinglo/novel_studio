import asyncio
import os
import sys

# Ensure app package is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.modules.outlines.engines.bible import BibleEngine


async def main():
    print("🚀 Reproducing Bible Generation Issue...")

    try:
        engine = BibleEngine()
        print("✅ BibleEngine initialized.")
    except Exception as e:
        print(f"❌ BibleEngine initialization failed: {e}")
        return

    # Mock history
    history = [
        "User: 我想写一本关于赛博朋克和修仙结合的小说。",
        "AI: 这个想法很有趣！赛博修仙通常会有很强烈的反差感。主角是什么身份？是底层黑客还是财团继承人？",
        "User: 主角是个底层黑客，但他意外捡到了一个上古修仙芯片。",
        "AI: 很好的切入点！金手指是上古芯片。那他的核心欲望是什么？复仇？长生？还是改变世界？",
        "User: 他想推翻控制世界的AI天道。",
        "AI: 对抗AI天道，非常有张力！那核心爽点是不是在于用古老的修仙法术降维打击高科技？",
        "User: 对，就是这个意思。",
    ]

    print(f"📊 Context: {len(history)} messages.")

    try:
        bible = await engine.generate(history)
        print("\n🎉 Generation Successful!")
        print(f"Title: {bible.title}")
        print(f"Logline: {bible.logline}")
        print(f"Hook: {bible.marketing_hook}")
    except Exception as e:
        print(f"\n❌ Generation Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
