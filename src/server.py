from fastmcp import FastMCP
import os
import argparse
from typing import List, Dict, Any
from pathlib import Path

# 创建FastMCP实例
mcp = FastMCP()

# 文档根目录
DOC_ROOT = Path(__file__).parent.parent / "document"
# UIKit文档目录
UIKIT_ROOT = Path(__file__).parent.parent / "uikit"

# 定义搜索文档的函数
@mcp.tool()
async def search_platform_docs(doc_type: str, platform: str = "") -> Dict[str, Any]:
    """
    搜索特定平台的文档目录
    
    参数:
    - doc_type: 文档类型，必填参数，只能为 'sdk' 或 'uikit'。
              'sdk': 搜索 document 目录下的文档
              'uikit': 搜索 uikit 目录下的文档
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
    try:
        # 验证doc_type参数
        if doc_type.lower() not in ["sdk", "uikit"]:
            return {
                "documents": [],
                "platform": platform,
                "count": 0,
                "error": f"无效的文档类型: {doc_type}，必须为 'sdk' 或 'uikit'"
            }
            
        # 平台名称映射字典
        platform_mapping = {
            "小程序": "applet",
            "鸿蒙": "harmonyos",
            "rn": "react-native",
            "rest": "server-side"
        }
        
        # 确保平台名是小写的，以便统一比较
        lowercasePlatform = platform.lower()
        doc_type = doc_type.lower()
        
        # 检查是否需要映射
        for key, value in platform_mapping.items():
            if key.lower() in lowercasePlatform:
                lowercasePlatform = value
                break
        
        results = []
        matchedPlatforms = []
        
        # 如果是搜索UIKit文档
        if doc_type == "uikit":
            if os.path.exists(UIKIT_ROOT) and os.path.isdir(UIKIT_ROOT):
                uikitDirs = []
                # 获取uikit下的所有子目录（如chatuikit, chatroomuikit等）
                for item in os.listdir(UIKIT_ROOT):
                    itemPath = os.path.join(UIKIT_ROOT, item)
                    if os.path.isdir(itemPath):
                        uikitDirs.append(item)
                
                # 检查是否有匹配的uikit子目录
                matchedUikitDirs = []
                if not platform:  # 如果没有指定平台，则包含所有uikit目录
                    matchedUikitDirs = uikitDirs
                    matchedPlatforms.append("uikit")
                else:
                    # 检查uikit子目录下是否有与platform匹配的平台目录
                    for uikitDir in uikitDirs:
                        if lowercasePlatform in uikitDir.lower():
                            matchedUikitDirs.append(uikitDir)
                            if "uikit" not in matchedPlatforms:
                                matchedPlatforms.append("uikit")
                            continue
                            
                        uikitDirPath = os.path.join(UIKIT_ROOT, uikitDir)
                        # 检查每个uikit子目录下的平台目录
                        if os.path.isdir(uikitDirPath):
                            platformDirs = [d for d in os.listdir(uikitDirPath) if os.path.isdir(os.path.join(uikitDirPath, d))]
                            for platformDir in platformDirs:
                                if lowercasePlatform and lowercasePlatform in platformDir.lower():
                                    matchedUikitDirs.append(uikitDir)
                                    if "uikit" not in matchedPlatforms:
                                        matchedPlatforms.append("uikit")
                                    break
                
                # 递归获取所有匹配的UIKit的Markdown文件
                for uikitDir in matchedUikitDirs:
                    uikitDirPath = os.path.join(UIKIT_ROOT, uikitDir)
                    for root, _, files in os.walk(uikitDirPath):
                        # 检查当前目录是否匹配指定的平台
                        if platform:
                            # 获取相对于uikitDir的路径
                            rel_to_uikit_dir = os.path.relpath(root, uikitDirPath)
                            # 如果不是根目录，检查第一级子目录是否匹配平台名
                            # 例如：chatuikit/android/xxx.md 中的 "android" 是否匹配指定的平台
                            if rel_to_uikit_dir != "." and rel_to_uikit_dir.split(os.sep)[0].lower() != lowercasePlatform:
                                continue
                                
                        for file in files:
                            if file.endswith('.md'):
                                fullPath = os.path.join(root, file)
                                # 转换为相对路径，添加uikit前缀
                                relPath = os.path.relpath(fullPath, UIKIT_ROOT)
                                results.append(f"uikit/{relPath}")
                
                # 包含uikit根目录下的md文件（如果没有指定平台或者是通用文档）
                if not platform:  # 只有在不指定平台时，才包含根目录下的MD文件
                    for file in os.listdir(UIKIT_ROOT):
                        if file.endswith('.md'):
                            fullPath = os.path.join(UIKIT_ROOT, file)
                            relPath = os.path.relpath(fullPath, UIKIT_ROOT)
                            results.append(f"uikit/{relPath}")
        
        # 如果是搜索SDK文档
        elif doc_type == "sdk":
            # 获取所有可用的平台目录
            if os.path.exists(DOC_ROOT) and os.path.isdir(DOC_ROOT):
                dirs = [d for d in os.listdir(DOC_ROOT) if os.path.isdir(os.path.join(DOC_ROOT, d))]
                
                # 过滤匹配的平台目录
                docMatchedPlatforms = []
                if not platform:  # 如果没有指定平台，包含所有平台
                    docMatchedPlatforms = dirs
                else:
                    docMatchedPlatforms = [d for d in dirs if lowercasePlatform in d.lower()]
                
                matchedPlatforms.extend(docMatchedPlatforms)
                
                # 收集所有匹配平台的文档
                for platformDir in docMatchedPlatforms:
                    platformPath = os.path.join(DOC_ROOT, platformDir)
                    
                    # 递归获取所有Markdown文件
                    for root, _, files in os.walk(platformPath):
                        for file in files:
                            if file.endswith('.md'):
                                fullPath = os.path.join(root, file)
                                # 转换为相对路径
                                relPath = os.path.relpath(fullPath, DOC_ROOT)
                                results.append(relPath)
        
        if not matchedPlatforms:
            return {
                "documents": [],
                "platform": platform,
                "count": 0,
                "error": f"未找到匹配平台: {platform}"
            }
        
        return {
            "documents": results,
            "platform": matchedPlatforms[0] if len(matchedPlatforms) == 1 else platform,
            "count": len(results),
            "error": None
        }
    except Exception as e:
        error_msg = f"搜索文档错误: {str(e)}"
        print(error_msg)
        return {
            "documents": [],
            "platform": platform,
            "count": 0,
            "error": error_msg
        }

# 定义获取文档内容的函数
@mcp.tool()
async def get_document_content(doc_path: str = "", keyword: str = "") -> Dict[str, Any]:
    """
    获取文档内容，并根据关键字搜索相关内容
    
    参数:
    - doc_path: 文档相对路径，例如 "android/quickstart.md" 或 "uikit/index.md"，必须提供
    - keyword: 搜索关键字（可选），如果提供则会在文档中搜索匹配的内容
    
    返回:
    {
        "content": str or None,  # 文档的完整内容，如果文档不存在或发生错误则为None
        "docPath": str,          # 请求的文档路径
        "matches": [             # 匹配结果列表，如果没有提供关键字或没有匹配则为空列表
            {
                "lineNumber": int,  # 匹配行的行号（从1开始）
                "context": str,     # 匹配行的上下文（包括前后各2行）
                "line": str         # 匹配的具体行内容
            },
            ...
        ],
        "error": str or None     # 错误信息，如果成功则为None
    }
    """
    try:
        # 确定文档路径
        if doc_path.startswith("uikit/"):
            # 处理UIKit文档
            relative_path = doc_path[6:]  # 移除 "uikit/" 前缀
            fullPath = os.path.join(UIKIT_ROOT, relative_path)
        else:
            # 处理普通文档
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
        error_msg = f"获取文档内容失败: {str(e)}"
        print(f"获取文档内容错误: {str(e)}")
        return {
            "content": None, 
            "docPath": doc_path,
            "matches": [],
            "error": error_msg
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
