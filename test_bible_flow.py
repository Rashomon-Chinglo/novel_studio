import asyncio
import sys
import os
import readline

# Ensure app package is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.modules.outlines.engines.bible import BibleEngine
except ImportError as e:
    print(f"Error importing BibleEngine: {e}")
    print(
        "Please ensure your PYTHONPATH is set correctly or you are running from the project root."
    )
    sys.exit(1)


async def main():
    print("🚀 [启动] Bible Flow 测试终端")
    print("---------------------------------------------------------")
    print("💡 指南：")
    print("1. 像和策划聊天一样输入你的想法。")
    print("2. 想要结束聊天并生成大纲时，请输入 'GEN' 或 '生成'。")
    print("3. 输入 'exit' 直接退出。")
    print("---------------------------------------------------------")

    try:
        engine = BibleEngine()
        print("✅ BibleEngine 初始化成功")
    except Exception as e:
        print(f"❌ BibleEngine 初始化失败 (请检查 .env 或 导入路径): {e}")
        return

    # 模拟前端维护的对话历史
    # 格式通常是 ["User: ...", "AI: ..."]
    history = []

    while True:
        # 1. 获取用户输入
        try:
            user_input = input("\n👤 User: ").strip()
        except EOFError:
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break

        # 2. 判断是否触发生成 (Trigger)
        if user_input.upper() == "GEN" or user_input == "生成":
            print("\n⚙️  [System] 用户触发生成指令...")
            print(f"📊 [Context] 将基于过去的 {len(history)} 条对话记录生成 Bible...")

            try:
                # 调用 "建筑师" Agent
                bible = await engine.generate(history)
                print(bible)

                print("\n🎉 ============ [DEEPNOVEL STORY BIBLE] ============ 🎉")
                print(f"📖 书名: 《{bible.title}》")
                print(f"📝 Logline: {bible.logline}")
                print("-" * 50)
                print(f"🔥 核心卖点 (Hook): \n   {bible.marketing_hook}")
                print("-" * 50)
                print(f"🌍 世界观基调 (Tone): \n   {bible.worldview_tone}")
                print("-" * 50)
                print(f"⚔️ 主线冲突: \n   {bible.main_conflict}")
                print("-" * 50)
                print(f"🏁 结局愿景: \n   {bible.ending_vision}")
                print("-" * 50)
                print(f"👥 人物关系简述: \n   {bible.key_roles_summary}")
                print("======================================================")
                break  # 生成完就结束测试
            except Exception as e:
                print(f"❌ 生成失败: {e}")
                import traceback

                traceback.print_exc()
                break

        # 3. 正常聊天流程 (Chat)
        print("🤖 AI (Thinking)...")
        try:
            # 调用 "引导员" Agent
            # 注意：history 是过去的记录，user_input 是当前的话
            response = await engine.brainstorm(history, user_input)

            # 清除 "Thinking..."
            print(" " * 20, end="\r")
            print(f"🤖 AI: {response}")

            # 4. 更新历史记录
            # 这一步非常关键！不仅为了下一轮聊天，也为了最后的生成
            history.append(f"User: {user_input}")
            history.append(f"AI: {response}")

        except Exception as e:
            print(f"\n❌ 聊天出错: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
