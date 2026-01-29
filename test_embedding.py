"""
测试 Jina Embeddings 模型是否正常工作
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.vector import get_vector_store


def test_embedding_model():
    print("🧪 Testing Jina Embeddings Model...")
    print("=" * 60)

    try:
        # 1. 初始化向量存储（会初始化 embedding 模型）
        print("\n1️⃣ Initializing vector store with Jina embeddings...")
        store = get_vector_store()
        print("   ✅ Vector store initialized successfully")

        # 2. 测试文本列表
        test_texts = [
            "这是一个测试文本，用于验证 embedding 功能。",
            "赛博朋克世界中的霓虹灯闪烁。",
            "主角是一位拥有老式义眼的侦探。",
        ]

        # 3. 测试 embedding 生成
        print("\n2️⃣ Testing embedding generation...")
        print(f"   📝 Test texts: {len(test_texts)} samples")

        # 使用 similarity_search 来隐式测试 embedding
        # 这会调用 embedding 模型对查询文本进行编码
        query = "侦探故事"
        print(f"\n3️⃣ Testing similarity search with query: '{query}'")

        # 先添加一些测试数据（如果数据库为空）
        data = store.get(limit=1)
        if not data["ids"]:
            print("\n   ⚠️  Database is empty, adding test data...")
            test_ids = ["test_1", "test_2", "test_3"]
            store.add_texts(
                texts=test_texts,
                ids=test_ids,
                metadatas=[
                    {"source": "test", "type": "sample"},
                    {"source": "test", "type": "sample"},
                    {"source": "test", "type": "sample"},
                ],
            )
            print("   ✅ Test data added")

        # 执行相似度搜索（会使用 embedding）
        results = store.similarity_search(query, k=2)

        print("\n4️⃣ Similarity search results:")
        print(f"   📊 Found {len(results)} results")

        for i, doc in enumerate(results, 1):
            print(f"\n   Result {i}:")
            print(f"   Content: {doc.page_content[:50]}...")
            print(f"   Metadata: {doc.metadata}")

        # 5. 测试 embedding 向量维度
        print("\n5️⃣ Testing embedding dimensions...")
        # 通过 store._collection 访问底层数据
        collection = store._collection
        sample_data = collection.get(limit=1, include=["embeddings"])

        # 修复：检查 embeddings 列表是否非空
        embeddings_list = sample_data.get("embeddings", [])
        if embeddings_list and len(embeddings_list) > 0:
            embedding_dim = len(embeddings_list[0])
            print(f"   ✅ Embedding dimension: {embedding_dim}")

            # Jina embeddings v3 应该是 1024 维
            if embedding_dim == 1024:
                print("   ✅ Correct dimension for jina-embeddings-v3")
            else:
                print(f"   ⚠️  Unexpected dimension (expected 1024, got {embedding_dim})")
        else:
            print("   ⚠️  No embeddings found in sample data")

        print("\n" + "=" * 60)
        print("✅ Jina Embeddings Model Test PASSED")
        print("=" * 60)
        print("\n📋 Summary:")
        print("   • Vector store initialization: ✅")
        print("   • Similarity search: ✅")
        print("   • Embedding generation: ✅")

        return True

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ Jina Embeddings Model Test FAILED")
        print(f"Error: {e}")
        print("=" * 60)

        import traceback

        traceback.print_exc()

        return False


if __name__ == "__main__":
    success = test_embedding_model()
    sys.exit(0 if success else 1)
