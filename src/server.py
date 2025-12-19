from fastmcp import FastMCP
import os
import argparse
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
from pydantic import Field
from functools import lru_cache

# 创建FastMCP实例
mcp = FastMCP()

# 文档根目录
DOC_ROOT = Path(__file__).parent.parent / "document"
# UIKit文档目录
UIKIT_ROOT = Path(__file__).parent.parent / "uikit"
# CallKit文档目录
CALLKIT_ROOT = Path(__file__).parent.parent / "callkit"

def _read_file_content(path: str) -> str:
    """同步读取文件内容"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

@lru_cache(maxsize=128)
def _scan_directory_docs(root_path: Path, platform: str, doc_type: str) -> tuple[List[str], List[str]]:
    """
    同步扫描文档目录
    root_path: 根目录路径
    platform: 规范化后的平台名称
    doc_type: 文档类型 (sdk/uikit/callkit)
    """
    results = []
    matched_platforms = []
    
    if not os.path.exists(root_path) or not os.path.isdir(root_path):
        return results, matched_platforms

    is_nested = doc_type in ["uikit", "callkit"]
    prefix_len = len(str(root_path)) + 1

    if is_nested:
        # UIKit/CallKit 处理逻辑 (嵌套结构)
        # 1. 查找符合条件的子模块 (如 chatuikit, chatroomuikit)
        top_dirs = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]
        target_subdirs = []
        
        if not platform:
            target_subdirs = top_dirs
            matched_platforms.append(doc_type)
        else:
            for d in top_dirs:
                # 检查目录名是否包含平台名
                if platform in d.lower():
                    target_subdirs.append(d)
                    if doc_type not in matched_platforms:
                        matched_platforms.append(doc_type)
                    continue
                
                # 检查子目录是否包含平台名
                sub_path = os.path.join(root_path, d)
                if os.path.exists(sub_path):
                    sub_sub_dirs = [sd for sd in os.listdir(sub_path) if os.path.isdir(os.path.join(sub_path, sd))]
                    for sd in sub_sub_dirs:
                        if platform in sd.lower():
                            target_subdirs.append(d)
                            if doc_type not in matched_platforms:
                                matched_platforms.append(doc_type)
                            break
        
        target_subdirs = list(set(target_subdirs))
        
        # 2. 遍历目标子模块
        for subdir in target_subdirs:
            subdir_path = os.path.join(root_path, subdir)
            for root, _, files in os.walk(subdir_path):
                # 平台过滤
                if platform:
                    rel_to_subdir = os.path.relpath(root, subdir_path)
                    if rel_to_subdir != ".":
                        # 检查第一级目录是否匹配平台
                        first_part = rel_to_subdir.split(os.sep)[0].lower()
                        # 原逻辑是非常严格的相等匹配或包含匹配？
                        # 原代码: rel_to_uikit_dir.split(os.sep)[0].lower() != lowercasePlatform
                        # 但这里的 platform 可能已经被映射过 (如 ios, android)
                        # 所以我们检查是否相等
                        if first_part != platform:
                            continue

                for file in files:
                    if file.endswith('.md'):
                        full_path = os.path.join(root, file)
                        # 结果格式: uikit/chatuikit/android/xxx.md
                        rel_path = full_path[prefix_len:]
                        results.append(f"{doc_type}/{rel_path}")

        # 3. 添加根目录文件 (仅当未指定平台时)
        if not platform:
            for file in os.listdir(root_path):
                if file.endswith('.md'):
                    results.append(f"{doc_type}/{file}")

    else:
        # SDK 处理逻辑 (扁平结构: document/android/...)
        top_dirs = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]
        target_dirs = []
        
        if not platform:
            target_dirs = top_dirs
            matched_platforms.extend(top_dirs)
        else:
            target_dirs = [d for d in top_dirs if platform in d.lower()]
            matched_platforms.extend(target_dirs)
            
        for d in target_dirs:
            dir_path = os.path.join(root_path, d)
            for root, _, files in os.walk(dir_path):
                for file in files:
                    if file.endswith('.md'):
                        full_path = os.path.join(root, file)
                        rel_path = full_path[prefix_len:]
                        results.append(rel_path)

    return results, matched_platforms

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
    搜索特定平台的文档目录。
    支持异步非阻塞执行和结果缓存。
    """
    try:
        if doc_type.lower() not in ["sdk", "uikit", "callkit"]:
            return {
                "documents": [],
                "platform": platform,
                "count": 0,
                "error": f"无效的文档类型: {doc_type}，必须为 'sdk'、'uikit' 或 'callkit'"
            }
            
        normalized_doc_type = doc_type.lower()
        normalized_platform = platform.lower()
        
        # 平台映射
        mapping = {}
        if normalized_doc_type == "uikit":
            mapping = {
                "小程序": "applet",
                "uni-app": "uniapp",
                "鸿蒙": "harmonyos",
                "rn": "react-native",
                "rest": "server-side"
            }
        else:
            mapping = {
                "小程序": "applet",
                "uni-app": "applet",
                "鸿蒙": "harmonyos",
                "rn": "react-native",
                "rest": "server-side"
            }
        
        for key, value in mapping.items():
            if key in normalized_platform:
                normalized_platform = value
                break
        
        # 确定根目录
        root_path = DOC_ROOT
        if normalized_doc_type == "uikit":
            root_path = UIKIT_ROOT
        elif normalized_doc_type == "callkit":
            root_path = CALLKIT_ROOT
            
        # 异步执行文件扫描（这是 CPU/IO 密集型操作，放入线程池）
        # 使用 asyncio.to_thread (Python 3.9+)
        documents, matched_platforms = await asyncio.to_thread(
            _scan_directory_docs, 
            root_path, 
            normalized_platform, 
            normalized_doc_type
        )
        
        # 构造返回结果
        result_platform = platform
        if matched_platforms:
             # 如果只有一个匹配平台，返回该平台；否则返回原始查询平台或第一个匹配项（逻辑保持原样）
             result_platform = matched_platforms[0] if len(matched_platforms) == 1 else platform
             if platform and platform == "":
                  # 如果未指定平台，可能返回 generic
                  pass

        if not documents and platform:
             return {
                "documents": [],
                "platform": platform,
                "count": 0,
                "error": f"未找到匹配平台: {platform}"
             }

        return {
            "documents": documents,
            "platform": result_platform,
            "count": len(documents),
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
async def get_document_content(
    doc_paths: Any = Field(
        default=None,
        description="文档相对路径列表，例如 [\"android/quickstart.md\", \"uikit/chatuikit/android/chatuikit_quickstart.md\"]，或者单个字符串路径"
    ),
    keyword: str = Field(
        default="",
        description="搜索关键字（可选），如果提供则会在文档中搜索匹配的内容，返回匹配行及其上下文"
    )
) -> Dict[str, Any]:
    """
    获取文档内容，并根据关键字搜索相关内容。
    使用异步 I/O 提高并发性能。
    """
    try:
        if doc_paths is None:
            doc_paths = []
        elif isinstance(doc_paths, str):
            doc_paths = [doc_paths]
        
        results = []
        total_matches = 0
        
        for doc_path in doc_paths:
            try:
                # 确定完整路径
                if doc_path.startswith("uikit/"):
                    full_path = UIKIT_ROOT / doc_path[6:]
                elif doc_path.startswith("callkit/"):
                    full_path = CALLKIT_ROOT / doc_path[8:]
                else:
                    full_path = DOC_ROOT / doc_path
                
                if not full_path.exists():
                    results.append({
                        "content": None, 
                        "docPath": doc_path,
                        "matches": [],
                        "error": "文档不存在"
                    })
                    continue
                
                # 异步读取文件
                content = await asyncio.to_thread(_read_file_content, str(full_path))
                
                # 处理内容
                content = content.replace('\t', '')
                matches = []
                
                if keyword and keyword.strip() != "":
                    lines = content.split('\n')
                    keyword_lower = keyword.lower()
                    
                    for i, line in enumerate(lines):
                        line_no_tabs = line.replace('\t', '')
                        if keyword_lower in line_no_tabs.lower():
                            start_line = max(0, i - 2)
                            end_line = min(len(lines) - 1, i + 2)
                            context = '\n'.join([lines[j].replace('\t', '') for j in range(start_line, end_line + 1)])
                            matches.append({
                                "lineNumber": i + 1,
                                "context": context,
                                "line": line_no_tabs
                            })
                
                results.append({
                    "content": content,
                    "docPath": doc_path,
                    "matches": matches,
                    "error": None
                })
                total_matches += len(matches)
                
            except Exception as e:
                error_msg = f"获取文档 {doc_path} 内容失败: {str(e)}"
                print(error_msg)
                results.append({
                    "content": None, 
                    "docPath": doc_path,
                    "matches": [],
                    "error": error_msg
                })
        
        return {
            "documents": results,
            "totalMatches": total_matches,
            "error": None if results else "未提供有效的文档路径"
        }
    except Exception as e:
        error_msg = f"获取文档内容失败: {str(e)}"
        print(f"获取文档内容错误: {str(e)}")
        return {
            "documents": [],
            "totalMatches": 0,
            "error": error_msg
        }

def main():
    """主函数，启动MCP服务器"""
    parser = argparse.ArgumentParser(description="环信文档搜索 MCP 服务")
    parser.add_argument("--transport", "-t", choices=["stdio", "http", "sse"], default="http", help="传输协议 (默认: http)")
    parser.add_argument("--host", default="0.0.0.0", help="HTTP传输时绑定的主机 (默认: 0.0.0.0)")
    parser.add_argument("--port", "-p", type=int, default=443, help="HTTP传输时绑定的端口 (默认: 443)")
    parser.add_argument("--path", default="/mcp/", help="HTTP传输时绑定的路径 (默认: /mcp/)")
    
    args = parser.parse_args()
    
    print(f"启动环信文档搜索MCP服务器 (已优化)")
    print(f"传输协议: {args.transport}")
    
    if args.transport in ["http", "sse"]:
        print(f"服务地址: http://{args.host}:{args.port}{args.path}")
    
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port, path=args.path)
    else:
        mcp.run(transport="http", host=args.host, port=args.port, path=args.path)

if __name__ == "__main__":
    main()
