from mcp import ClientSessionGroup
from mcp.client.session_group import StreamableHttpParameters
import asyncio
import json

async def test_json_format():
    """测试 search_platform_docs 返回的是否是有效的 JSON 格式"""
    print("=== 测试 search_platform_docs 返回格式 ===")
    
    # 创建 MCP 客户端
    async with ClientSessionGroup() as group:
        # 连接到服务器
        server_params = StreamableHttpParameters(
            url="http://127.0.0.1:9000/mcp/"
        )
        session = await group.connect_to_server(server_params)
    
        try:
            # 调用 search_platform_docs API
            print("调用 search_platform_docs API...")
            docs_result = await group.call_tool("search_platform_docs", {"platform": "android"})
            
            # 检查结果类型
            print(f"返回结果类型: {type(docs_result)}")
            
            # 尝试解析为 JSON
            if hasattr(docs_result, "content") and docs_result.content:
                raw_text = docs_result.content[0].text
                print(f"原始文本前100个字符: {raw_text[:100]}...")
                
                try:
                    # 尝试解析为 JSON
                    result_json = json.loads(raw_text)
                    print("✅ 成功解析为 JSON 格式!")
                    
                    # 验证 JSON 结构
                    if isinstance(result_json, dict):
                        print("✅ 返回结果是一个 JSON 对象")
                        
                        # 检查必要的字段
                        required_fields = ["documents", "platform", "count", "error"]
                        missing_fields = [field for field in required_fields if field not in result_json]
                        
                        if not missing_fields:
                            print("✅ 包含所有必要字段: documents, platform, count, error")
                        else:
                            print(f"❌ 缺少字段: {', '.join(missing_fields)}")
                        
                        # 检查 documents 字段是否为列表
                        if "documents" in result_json and isinstance(result_json["documents"], list):
                            print(f"✅ documents 字段是列表，包含 {len(result_json['documents'])} 个文档")
                        else:
                            print("❌ documents 字段不是列表或不存在")
                    else:
                        print(f"❌ 返回结果不是 JSON 对象，而是 {type(result_json)}")
                    
                except json.JSONDecodeError as e:
                    print(f"❌ 不是有效的 JSON 格式: {e}")
            else:
                print("❌ 返回结果没有内容")
                
        except Exception as e:
            print(f"❌ 测试过程中出错: {e}")

# 运行测试
if __name__ == "__main__":
    asyncio.run(test_json_format())
