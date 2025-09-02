from fastmcp import FastMCP
import os
import argparse
from typing import List, Dict, Any
from pathlib import Path

# 创建FastMCP实例
mcp = FastMCP()

# 文档根目录
DOC_ROOT = Path(__file__).parent.parent / "document"

# 定义搜索文档的函数
@mcp.tool()
async def search_platform_docs(platform: str) -> List[str]:
    """
    搜索特定平台的文档目录
    
    参数:
    - platform: 平台名称，如 'android', 'ios', 'web' 等
    
    返回:
    - 匹配的文档路径列表
    """
    try:
        # 确保平台名是小写的，以便统一比较
        lowercasePlatform = platform.lower()
        
        # 获取所有可用的平台目录
        dirs = [d for d in os.listdir(DOC_ROOT) if os.path.isdir(os.path.join(DOC_ROOT, d))]
        
        # 过滤匹配的平台目录
        matchedPlatforms = [d for d in dirs if lowercasePlatform in d.lower()]
        
        if not matchedPlatforms:
            return []
        
        # 收集所有匹配平台的文档
        results = []
        
        for platformDir in matchedPlatforms:
            platformPath = os.path.join(DOC_ROOT, platformDir)
            
            # 递归获取所有Markdown文件
            for root, _, files in os.walk(platformPath):
                for file in files:
                    if file.endswith('.md'):
                        fullPath = os.path.join(root, file)
                        # 转换为相对路径
                        relPath = os.path.relpath(fullPath, DOC_ROOT)
                        results.append(relPath)
        
        return results
    except Exception as e:
        print(f"搜索文档错误: {str(e)}")
        return []

# 定义获取文档内容的函数
@mcp.tool()
async def get_document_content(doc_path: str, keyword: str = "") -> Dict[str, Any]:
    """
    获取文档内容，并根据关键字搜索相关内容
    
    参数:
    - doc_path: 文档相对路径
    - keyword: 搜索关键字（可选）
    
    返回:
    - 包含文档内容和匹配片段的字典
    """
    try:
        fullPath = os.path.join(DOC_ROOT, doc_path)
        
        # 检查文件是否存在
        if not os.path.exists(fullPath):
            return {
                "content": None, 
                "docPath": doc_path,
                "matches": [],
                "error": "文档不存在"
            }
        
        # 读取文件内容
        with open(fullPath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果没有关键字，返回全部内容
        if not keyword or keyword.strip() == "":
            return {
                "content": content,
                "docPath": doc_path,
                "matches": [],
                "error": None
            }
        
        # 搜索关键字
        lines = content.split('\n')
        matches = []
        
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                # 提取匹配行的上下文（前后各2行）
                startLine = max(0, i - 2)
                endLine = min(len(lines) - 1, i + 2)
                
                context = '\n'.join(lines[startLine:endLine + 1])
                matches.append({
                    "lineNumber": i + 1,
                    "context": context,
                    "line": line
                })
        
        return {
            "content": content,
            "docPath": doc_path,
            "matches": matches,
            "error": None
        }
    except Exception as e:
        print(f"获取文档内容错误: {str(e)}")
        return {
            "content": None, 
            "docPath": doc_path,
            "matches": [],
            "error": f"获取文档内容失败: {str(e)}"
        }

def main():
    """主函数，启动MCP服务器"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="环信文档搜索 MCP 服务")
    parser.add_argument(
        "--transport", "-t",
        choices=["stdio", "http", "sse"],
        default="http",
        help="传输协议 (默认: http)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="HTTP传输时绑定的主机 (默认: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=443,
        help="HTTP传输时绑定的端口 (默认: 443)"
    )
    parser.add_argument(
        "--path",
        default="/mcp/",
        help="HTTP传输时绑定的路径 (默认: /mcp/)"
    )
    
    args = parser.parse_args()
    
    print(f"启动环信文档搜索MCP服务器")
    print(f"传输协议: {args.transport}")
    if args.transport in ["http", "sse"]:
        print(f"主机: {args.host}")
        print(f"端口: {args.port}")
        print(f"路径: {args.path}")
        print(f"服务地址: http://{args.host}:{args.port}{args.path}")
    
    # 根据传输协议启动服务器
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "sse":
        mcp.run(
            transport="sse",
            host=args.host,
            port=args.port,
            path=args.path
        )
    else:  # http
        mcp.run(
            transport="http",
            host=args.host,
            port=args.port,
            path=args.path
        )

# 主入口点
if __name__ == "__main__":
    main()
