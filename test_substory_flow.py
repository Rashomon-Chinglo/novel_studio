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
    print(
        "Please ensure your PYTHONPATH is set correctly or you are running from the project root."
    )
    sys.exit(1)


# Create a dummy Bible for testing context
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
    print("🚀 [启动] Substory Flow 测试终端")
    print("---------------------------------------------------------")
    print(f"📚 基于 Bible: 《{DUMMY_BIBLE.title}》")
    print("---------------------------------------------------------")
    print("💡 指南：")
    print("1. 输入关于这一卷/这一部分剧情的想法 (分卷/大情节)。")
    print("2. 想要结束聊天并生成分卷大纲时，请输入 'GEN' 或 '生成'。")
    print("3. 输入 'exit' 直接退出。")
    print("---------------------------------------------------------")

    try:
        engine = SubstoryEngine()
        print("✅ SubstoryEngine 初始化成功")
    except Exception as e:
        print(f"❌ SubstoryEngine 初始化失败: {e}")
        return

    # 模拟前端维护的对话历史
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
            print(f"📊 [Context] 将基于过去的 {len(history)} 条对话记录生成 Substory...")

            try:
                context = engine.SubstoryGenerateContext(history=history, bible=DUMMY_BIBLE)
                substory = await engine.generate(context)

                print("\n🎉 ============ [SUBSTORY GENERATED] ============ 🎉")
                print(f"📑 篇章标题: {substory.substory_title}")
                print("-" * 50)
                print(f"⚔️ 核心冲突: {substory.core_conflict}")
                print("-" * 50)
                print(f"🔄 状态变化: {substory.status_change}")
                print("-" * 50)
                print("🔗 逻辑链条 (Logic Nodes):")
                for i, node in enumerate(substory.logic_nodes, 1):
                    print(f"\n  [{i}]")
                    print(f"  Cause   : {node.cause}")
                    print(f"  Process : {node.process}")
                    print(f"  Effect  : {node.effect}")
                    print(f"  Exchange: {node.exchange}")
                    if node.context:
                        print(f"  Context : {node.context}")
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
            context = engine.SubstoryBrainstormContext(
                history=history, user_input=user_input, bible=DUMMY_BIBLE
            )
            response = await engine.brainstorm(context)
            print(response)
            # 清除 "Thinking..."
            print(" " * 20, end="\r")
            print(f"🤖 AI: {response}")

            # 4. 更新历史记录
            history.append(f"User: {user_input}")
            history.append(f"AI: {response}")

        except Exception as e:
            print(f"\n❌ 聊天出错: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
