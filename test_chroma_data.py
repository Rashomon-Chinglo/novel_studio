# inspect_db.py
import argparse
import collections
import os
import sys
import time

# 路径修补
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.vector import get_vector_store


def get_store():
    try:
        return get_vector_store()
    except Exception as e:
        print(f"❌ [致命错误] 无法连接向量库: {e}")
        sys.exit(1)


# ==========================================
# 👇 核心：一键诊断逻辑
# ==========================================


def cmd_diagnose(args):
    print("\n🏥 [Novel Studio 数据库全面体检开始] ------------------")
    store = get_store()

    # 1. 连接与容量检查
    print("\n1️⃣  [基础连通性检查]")
    try:
        # 为了不消耗太多内存，这里只取 ids
        ids = store.get()["ids"]
        total_count = len(ids)
        print("   ✅ 连接成功")
        print(f"   📊 当前数据总量: {total_count} 条片段")

        if total_count == 0:
            print("   ⚠️  警告: 数据库是空的！请先运行 mining 流程。")
            print("   🚫体检提前结束")
            return

        # 再拿一条完整的做抽样
        data = store.get(limit=1)
    except Exception as e:
        print(f"   ❌ 获取数据失败: {e}")
        return

    # 2. 数据完整性检查 (抽样)
    print("\n2️⃣  [数据完整性抽查]")
    # 随机抽样太麻烦，直接拿第一条做演示即可，只要结构对就行
    sample_meta = data["metadatas"][0]
    sample_doc = data["documents"][0]

    missing_fields = []
    for field in ["title", "category", "tags"]:
        if field not in sample_meta:
            missing_fields.append(field)

    if not missing_fields:
        print("   ✅ 元数据结构正常 (包含 title, category, tags)")
    else:
        print(f"   ❌ 发现缺失字段: {missing_fields}")

    if len(sample_doc) < 10:
        print("   ⚠️  警告: 抽样片段内容过短 (<10字)，可能是脏数据")
    else:
        print("   ✅ 文本内容长度正常")

    # 3. 向量搜索能力回测 (Top 3)
    print("\n3️⃣  [Jina 向量检索能力回测 (Top 3)]")
    # test_query = sample_doc[:50]
    test_query = "追赶"
    print(f"   🧪 测试 Query: '{test_query}'")

    start_time = time.time()
    # 👇 改动：这里改成 k=3
    results = store.similarity_search(test_query, k=3)
    end_time = time.time()

    if results:
        # 验证第一名是否是自己
        top_res = results[0]
        if top_res.page_content[:20] == sample_doc[:20]:
            print("   ✅ 回测成功 (Rank 1 精准命中)")
            print(f"   ⚡ 响应耗时: {(end_time - start_time) * 1000:.2f} ms")
        else:
            print("   ⚠️  回测漂移: 第一名不是原片段 (可能是语义极其相似的片段)")

        # 👇 改动：展示 Top 3 详情
        print("\n   📄 [Top 3 命中详情]")
        for i, res in enumerate(results):
            print(f"   {'=' * 10} Rank {i + 1} {'=' * 10}")
            # 限制打印长度，防止刷屏
            content_preview = res.page_content.replace("\n", " ")

            print(f"   📝 内容: {content_preview}")
            print(
                f"   🏷️  来源: 《{res.metadata.get('title')}》 | 标签: {res.metadata.get('tags')}"
            )

    else:
        print("   ❌ 搜索失败: 返回结果为空")

    # 4. 分布统计
    print("\n4️⃣  [数据分布概览]")
    # 重新获取一次只包含 metadatas 的全量数据用于统计
    all_metas = store.get(include=["metadatas"])["metadatas"]
    books = [m.get("title", "未知") for m in all_metas]
    book_counts = collections.Counter(books)

    for book, count in book_counts.items():
        print(f"   📘 《{book}》: {count} 条")

    print(
        "\n✅ [体检结束] 系统运行良好"
        if total_count > 0
        else "\n⚠️ [体检结束] 系统存在问题"
    )


# ==========================================
# 👇 旧的独立命令 (保留给你备用)
# ==========================================
def cmd_search(args):
    store = get_store()
    print(f"🔎 搜索: [{args.query}]")
    results = store.similarity_search(args.query, k=3)
    for i, res in enumerate(results):
        print(f"{i + 1}. {res.page_content[:30]}... (《{res.metadata.get('title')}》)")


def cmd_peek(args):
    store = get_store()
    data = store.get(limit=5)
    for i in range(len(data["ids"])):
        print(
            f"📄 [{data['metadatas'][i].get('title')}] {data['documents'][i][:30]}..."
        )


def cmd_clean(args):
    store = get_store()
    print(f"正在删除《{args.book}》...")
    data = store.get(where={"title": args.book})
    if data["ids"]:
        store.delete(ids=data["ids"])
        print(f"✅ 已删除 {len(data['ids'])} 条记录")
    else:
        print("未找到数据")


# ==========================================
# 👇 主入口
# ==========================================
def main():
    parser = argparse.ArgumentParser(description="Novel Studio 数据库全能管家")
    subparsers = parser.add_subparsers(dest="command", help="命令模式")

    # 默认命令 (如果不输入参数，默认跑诊断)
    # 注意：argparse 默认不支持无参自动选子命令，需要在下面处理

    # 1. 诊断 (Auto Check)
    subparsers.add_parser("auto", help="一键全自动体检")

    # 2. 其他命令
    search_parser = subparsers.add_parser("search", help="搜索测试")
    search_parser.add_argument("query", type=str)

    subparsers.add_parser("peek", help="查看前5条")

    clean_parser = subparsers.add_parser("clean", help="删除书籍")
    clean_parser.add_argument("book", type=str)

    # 兼容处理：如果没有输入任何参数，默认执行 auto
    if len(sys.argv) == 1:
        args = parser.parse_args(["auto"])
    else:
        args = parser.parse_args()

    if args.command == "auto":
        cmd_diagnose(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "peek":
        cmd_peek(args)
    elif args.command == "clean":
        cmd_clean(args)


if __name__ == "__main__":
    main()
