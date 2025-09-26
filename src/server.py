from fastmcp import FastMCP
import argparse
from typing import List, Dict, Any
from pydantic import Field

# 导入service模块中的功能
from service import search_platform_docs as service_search_platform_docs
from service import get_document_content as service_get_document_content

# 创建FastMCP实例
mcp = FastMCP()

# 定义搜索文档的函数
@mcp.tool()
async def search_platform_docs(
    doc_type: str = Field(
        default="sdk",
        description="文档类型，必填参数，可选值为 'sdk'、'uikit' 或 'callkit'。'sdk'表示搜索document目录下的文档，'uikit'表示搜索uikit目录下的文档，'callkit'表示搜索callkit目录下的文档"
    ),
    platform: str = Field(
        default="",
        description="平台名称，如android、ios、web等。支持部分匹配，如输入'and'会匹配'android'。支持映射：小程序->applet、鸿蒙->harmonyos"
    )
) -> Dict[str, Any]:
    """
    搜索特定平台的文档目录
    
    参数:
    - doc_type: 文档类型，必填参数，可选值为 'sdk'、'uikit' 或 'callkit'。
              'sdk': 搜索 document 目录下的文档
              'uikit': 搜索 uikit 目录下的文档
              'callkit': 搜索 callkit 目录下的文档
    - platform: 平台名称，如 'android', 'ios', 'web', 'flutter', 'react-native', 'applet', 'server-side', 'uikit' 等。
              支持部分匹配，例如输入 'and' 会匹配 'android'。
              支持常用词语映射：'小程序' -> 'applet', '鸿蒙' -> 'harmonyos', 'rn' -> 'react-native', 'rest' -> 'server-side'
              
              当指定平台时，将只返回该平台的文档。例如：
              - 当 doc_type='uikit' 且 platform='android' 时，只返回 uikit 下 android 目录中的文档
              - 当 doc_type='sdk' 且 platform='ios' 时，只返回 document/ios 目录下的文档
    
    返回:
    {
        "documents": [            # 文档路径列表
            "android/quickstart.md",
            "android/integration.md",
            ...
        ],
        "platform": "android",    # 匹配的平台名称
        "count": 42,             # 找到的文档数量
        "error": null            # 错误信息，成功时为null
    }
    
    如果没有找到匹配的平台或发生错误，则返回:
    {
        "documents": [],
        "platform": "输入的平台名",
        "count": 0,
        "error": "错误信息或未找到匹配平台"
    }
    """
    # 调用service模块中的实现
    return service_search_platform_docs(doc_type, platform)

# 定义获取文档内容的函数
@mcp.tool()
async def get_document_content(
    doc_paths: List[str] = Field(
        default=None,
        description="文档相对路径列表，例如 [\"android/quickstart.md\", \"uikit/chatuikit/android/chatuikit_quickstart.md\"]，如果提供单个字符串，将自动转换为列表"
    ),
    keyword: str = Field(
        default="",
        description="搜索关键字（可选），如果提供则会在文档中搜索匹配的内容，返回匹配行及其上下文"
    )
) -> Dict[str, Any]:
    """
    获取文档内容，并根据关键字搜索相关内容
    
    参数:
    - doc_paths: 文档相对路径列表，例如 ["android/quickstart.md", "uikit/chatuikit/android/chatuikit_quickstart.md"]
                如果提供单个字符串，将自动转换为列表
    - keyword: 搜索关键字（可选），如果提供则会在文档中搜索匹配的内容
    
    返回:
    {
        "documents": [           # 文档内容列表
            {
                "content": str or None,  # 文档的完整内容，如果文档不存在或发生错误则为None
                "docPath": str,          # 文档路径
                "matches": [             # 匹配结果列表，如果没有提供关键字或没有匹配则为空列表
                    {
                        "lineNumber": int,  # 匹配行的行号（从1开始）
                        "context": str,     # 匹配行的上下文（包括前后各2行）
                        "line": str         # 匹配的具体行内容
                    },
                    ...
                ],
                "error": str or None     # 错误信息，如果成功则为None
            },
            ...
        ],
        "totalMatches": int,     # 所有文档中匹配的总数
        "error": str or None     # 整体错误信息，如果成功则为None
    }
    """
    # 调用service模块中的实现
    return service_get_document_content(doc_paths, keyword)

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