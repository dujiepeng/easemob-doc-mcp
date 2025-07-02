#!/usr/bin/env python3
"""
FastMCP文档搜索服务 - MCP运行脚本
"""
from main import mcp

if __name__ == "__main__":
    print("启动FastMCP文档搜索服务...")
    print("可在Cursor中配置以下信息:")
    print("- 端点: stdio")
    print("- 名称: 文档搜索服务")
    print("- 说明: 搜索文档内容并获取文档")
    print("- 可用工具:")
    print("  - search_platform_docs(platform: str) - 搜索特定平台的文档")
    print("  - get_document_content(doc_path: str, keyword: str = \"\") - 获取文档内容和关键字搜索结果")
    
    # 运行FastMCP服务
    mcp.run() 