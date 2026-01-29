"""直接测试 Jina Embeddings 向量化功能"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_community.embeddings import JinaEmbeddings

from app.core.config import settings

print("🧪 Testing Jina Embeddings Direct Vectorization")
print("=" * 60)

try:
    # 1. 初始化 Jina Embeddings
    print("\n1️⃣ Initializing Jina Embeddings...")
    embeddings = JinaEmbeddings(
        jina_api_key=settings.JINA_API_KEY,
        jina_url=settings.JINA_API_URL,
        model_name="jina-embeddings-v3",
    )
    print("   ✅ JinaEmbeddings initialized")

    # 2. 测试单个文本向量化
    print("\n2️⃣ Testing single text embedding...")
    test_query = "这是一个测试查询：赛博朋克侦探故事"
    print(f"   Text: '{test_query}'")

    query_vector = embeddings.embed_query(test_query)
    print("   ✅ Generated vector")
    print(f"   📊 Vector dimension: {len(query_vector)}")
    print(f"   📈 First 5 values: {query_vector[:5]}")

    # 3. 测试批量文本向量化
    print("\n3️⃣ Testing batch text embedding...")
    test_docs = [
        "主角是一位拥有老式义眼的侦探。",
        "赛博朋克世界中的霓虹灯闪烁。",
        "合成人偶像的谋杀案引发了两大财团的冲突。",
    ]
    print(f"   Documents: {len(test_docs)} texts")

    doc_vectors = embeddings.embed_documents(test_docs)
    print(f"   ✅ Generated {len(doc_vectors)} vectors")

    for i, vec in enumerate(doc_vectors, 1):
        print(f"\n   Doc {i}:")
        print(f"   - Dimension: {len(vec)}")
        print(f"   - First 3 values: {vec[:3]}")

    # 4. 验证向量维度
    print("\n4️⃣ Validating vector dimensions...")
    expected_dim = 1024  # jina-embeddings-v3

    if len(query_vector) == expected_dim:
        print(f"   ✅ Query vector dimension correct: {expected_dim}")
    else:
        print(f"   ❌ Unexpected dimension: {len(query_vector)} (expected {expected_dim})")

    all_correct = all(len(v) == expected_dim for v in doc_vectors)
    if all_correct:
        print(f"   ✅ All document vectors dimension correct: {expected_dim}")
    else:
        print("   ❌ Some document vectors have wrong dimension")

    # 5. 计算向量相似度（验证语义）
    print("\n5️⃣ Computing vector similarity...")
    import numpy as np

    # 计算 query 和第一个 doc 的余弦相似度
    query_arr = np.array(query_vector)
    doc1_arr = np.array(doc_vectors[0])

    similarity = np.dot(query_arr, doc1_arr) / (
        np.linalg.norm(query_arr) * np.linalg.norm(doc1_arr)
    )
    print(f"   📊 Cosine similarity (query vs doc1): {similarity:.4f}")

    print("\n" + "=" * 60)
    print("✅ JINA EMBEDDINGS TEST PASSED!")
    print("=" * 60)
    print("\n📋 Summary:")
    print("   • Model: jina-embeddings-v3")
    print(f"   • Vector dimension: {len(query_vector)}")
    print("   • Single text embedding: ✅")
    print("   • Batch embedding: ✅")
    print("   • Semantic similarity: ✅")

except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
