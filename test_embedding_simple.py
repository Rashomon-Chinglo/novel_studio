"""简单的 Jina Embeddings 测试"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.vector import get_vector_store

print("🧪 Testing Jina Embeddings Model...")
print("=" * 60)

try:
    # 1. 初始化
    print("\n1️⃣ Initializing...")
    store = get_vector_store()
    print("   ✅ Vector store initialized")
    
    # 2. 测试搜索
    print("\n2️⃣ Testing similarity search...")
    results = store.similarity_search("侦探", k=2)
    print(f"   ✅ Found {len(results)} results")
    
    for i, doc in enumerate(results, 1):
        print(f"\n   [{i}] {doc.page_content[:40]}...")
    
    # 3. 检查维度
    print("\n3️⃣ Checking embedding dimensions...")
    collection = store._collection
    data = collection.get(limit=1, include=["embeddings"])
    emb_list = data.get("embeddings")
    
    if emb_list is not None and isinstance(emb_list, list) and len(emb_list) > 0:
        dim = len(emb_list[0])
        print(f"   ✅ Embedding dim: {dim}")
        if dim == 1024:
            print(f"   ✅ Correct for jina-embeddings-v3")
    
    print("\n" + "=" * 60)
    print("✅ TEST PASSED - Jina Embeddings working!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
