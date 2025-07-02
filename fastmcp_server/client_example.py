from fastmcp import FastMCPClient

# 创建FastMCP客户端实例
client = FastMCPClient("http://localhost:8000")

async def example_usage():
    """示例使用FastMCP客户端进行文档搜索"""
    print("FastMCP文档搜索客户端示例")
    
    # 示例1: 搜索Android平台文档
    print("\n--- 搜索Android平台文档 ---")
    android_docs = await client.search_platform_docs(platform="android")
    print(f"找到 {len(android_docs)} 个Android文档:")
    for i, doc in enumerate(android_docs[:5], 1):  # 只显示前5个结果
        print(f"{i}. {doc}")
    if len(android_docs) > 5:
        print(f"...以及 {len(android_docs) - 5} 个更多文档")
    
    # 示例2: 获取特定文档内容
    if android_docs:
        doc_path = android_docs[0]  # 使用第一个文档作为示例
        print(f"\n--- 获取文档内容: {doc_path} ---")
        doc_content = await client.get_document_content(doc_path=doc_path)
        
        # 显示文档标题和部分内容
        content_lines = doc_content["content"].split("\n")
        title = next((line for line in content_lines if line.startswith("# ")), "无标题")
        print(f"标题: {title}")
        print(f"内容预览: {content_lines[min(5, len(content_lines) - 1)][:100]}...")
    
    # 示例3: 在文档中搜索关键字
    if android_docs:
        doc_path = android_docs[0]
        keyword = "初始化"
        print(f"\n--- 在文档中搜索关键字: '{keyword}' ---")
        search_results = await client.get_document_content(doc_path=doc_path, keyword=keyword)
        
        # 显示匹配结果
        matches = search_results.get("matches", [])
        print(f"找到 {len(matches)} 个匹配:")
        for i, match in enumerate(matches[:3], 1):  # 只显示前3个结果
            print(f"{i}. 行 {match['lineNumber']}: {match['line'][:80]}...")

if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage()) 