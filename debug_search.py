import sys
import os
import asyncio
from pathlib import Path

# 确保能导入 src 模块
sys.path.append(os.getcwd())

try:
    from src.indexer import build_index_async, global_indexer
except ImportError as e:
    print(f"错误: 无法导入 src.indexer。详细信息: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

async def main():
    print("🔍 正在初始化搜索引擎 (Whoosh + Jieba)...")
    
    # 1. 定义文档路径
    ROOT = Path(__file__).parent
    DOC_ROOT = ROOT / "document"
    UIKIT_ROOT = ROOT / "uikit"
    CALLKIT_ROOT = ROOT / "callkit"

    # 2. 构建索引
    # rebuild=False: 如果索引存在则直接使用，加快调试速度
    await build_index_async(DOC_ROOT, UIKIT_ROOT, CALLKIT_ROOT, rebuild=False)
    print("\n✅ 索引构建完成！\n")
    
    # 3. 定义测试查询
    test_cases = [
        {"query": "如何集成", "platform": "android", "desc": "搜索 Android 下的 '如何集成'"},
        {"query": "登录失效", "platform": None, "desc": "全局搜索 '登录失效' (验证中文分词)"},
        {"query": "push notification", "platform": "ios", "desc": "搜索 iOS 下的 'push notification'"}
    ]

    # 4. 执行搜索并打印结果
    for case in test_cases:
        q = case["query"]
        p = case["platform"]
        print(f"TEST CASE: {case['desc']}")
        print(f"Query: '{q}' | Platform: {p}")
        print("-" * 60)
        
        results = global_indexer.search(q, limit=3, platform=p)
        
        if not results:
            print("  (无匹配结果)")
        
        for i, doc in enumerate(results):
            print(f"  Result #{i+1} [Score: {doc['score']:.2f}]")
            print(f"  Title: {doc['title']}")
            print(f"  Path:  {doc['path']}")
            # 清理一下摘要中的换行，让显示更整洁
            summary = doc['summary'].replace('\n', ' ')
            print(f"  Match: ...{summary}...")
            print("")
        print("=" * 60 + "\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n已停止")
