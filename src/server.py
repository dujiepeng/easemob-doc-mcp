from fastmcp import FastMCP
import os
import argparse
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
from pydantic import Field
from functools import lru_cache
from .indexer import global_indexer, build_index_async  # 导入索引模块

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
    """
    results = []
    matched_platforms = []
    
    if not os.path.exists(root_path) or not os.path.isdir(root_path):
        return results, matched_platforms

    is_nested = doc_type in ["uikit", "callkit"]
    prefix_len = len(str(root_path)) + 1

    if is_nested:
        top_dirs = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]
        target_subdirs = []
        
        if not platform:
            target_subdirs = top_dirs
            matched_platforms.append(doc_type)
        else:
            for d in top_dirs:
                if platform in d.lower():
                    target_subdirs.append(d)
                    if doc_type not in matched_platforms:
                        matched_platforms.append(doc_type)
                    continue
                
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
        
        for subdir in target_subdirs:
            subdir_path = os.path.join(root_path, subdir)
            for root, _, files in os.walk(subdir_path):
                if platform:
                    rel_to_subdir = os.path.relpath(root, subdir_path)
                    if rel_to_subdir != ".":
                        first_part = rel_to_subdir.split(os.sep)[0].lower()
                        if first_part != platform:
                            continue

                for file in files:
                    if file.endswith('.md'):
                        full_path = os.path.join(root, file)
                        rel_path = full_path[prefix_len:]
                        results.append(f"{doc_type}/{rel_path}")

        if not platform:
            for file in os.listdir(root_path):
                if file.endswith('.md'):
                    results.append(f"{doc_type}/{file}")

    else:
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

@mcp.tool()
async def search_platform_docs(
    doc_type: str = Field(
        default="sdk",
        description="文档类型，必填参数，可选值为 'sdk'、'uikit' 或 'callkit'"
    ),
    platform: str = Field(
        default="",
        description="平台名称，如android、ios等"
    )
) -> Dict[str, Any]:
    """
    搜索特定平台的文档目录 (传统文件名列表搜索)。
    """
    try:
        if doc_type.lower() not in ["sdk", "uikit", "callkit"]:
            return {"documents": [], "error": f"无效的文档类型: {doc_type}"}
            
        normalized_doc_type = doc_type.lower()
        normalized_platform = platform.lower()
        
        mapping = {}
        if normalized_doc_type == "uikit":
            mapping = {
                "小程序": "applet", "uni-app": "uniapp", "鸿蒙": "harmonyos", 
                "rn": "react-native", "rest": "server-side"
            }
        else:
            mapping = {
                "小程序": "applet", "uni-app": "applet", "鸿蒙": "harmonyos", 
                "rn": "react-native", "rest": "server-side"
            }
        
        for key, value in mapping.items():
            if key in normalized_platform:
                normalized_platform = value
                break
        
        root_path = DOC_ROOT
        if normalized_doc_type == "uikit":
            root_path = UIKIT_ROOT
        elif normalized_doc_type == "callkit":
            root_path = CALLKIT_ROOT
            
        documents, matched_platforms = await asyncio.to_thread(
            _scan_directory_docs, root_path, normalized_platform, normalized_doc_type
        )
        
        result_platform = matched_platforms[0] if len(matched_platforms) == 1 else platform

        return {
            "documents": documents,
            "platform": result_platform,
            "count": len(documents),
            "error": None
        }

    except Exception as e:
        return {"documents": [], "error": f"搜索文档错误: {str(e)}"}

@mcp.tool()
async def get_document_content(
    doc_paths: Any = Field(default=None, description="文档相对路径列表"),
    keyword: str = Field(default="", description="搜索关键字")
) -> Dict[str, Any]:
    """获取文档内容"""
    try:
        if doc_paths is None:
            doc_paths = []
        elif isinstance(doc_paths, str):
            doc_paths = [doc_paths]
        
        results = []
        total_matches = 0
        
        for doc_path in doc_paths:
            try:
                if doc_path.startswith("uikit/"):
                    full_path = UIKIT_ROOT / doc_path[6:]
                elif doc_path.startswith("callkit/"):
                    full_path = CALLKIT_ROOT / doc_path[8:]
                else:
                    full_path = DOC_ROOT / doc_path
                
                if not full_path.exists():
                    results.append({"error": "文档不存在", "docPath": doc_path})
                    continue
                
                content = await asyncio.to_thread(_read_file_content, str(full_path))
                content = content.replace('\t', '')
                matches = []
                
                if keyword and keyword.strip() != "":
                    lines = content.split('\n')
                    keyword_lower = keyword.lower()
                    for i, line in enumerate(lines):
                        line_no_tabs = line.replace('\t', '')
                        if keyword_lower in line_no_tabs.lower():
                            start = max(0, i - 2)
                            end = min(len(lines) - 1, i + 2)
                            context = '\n'.join([lines[j].replace('\t', '') for j in range(start, end + 1)])
                            matches.append({
                                "lineNumber": i + 1,
                                "context": context,
                                "line": line_no_tabs
                            })
                
                results.append({
                    "content": content,
                    "docPath": doc_path,
                    "matches": matches
                })
                total_matches += len(matches)
                
            except Exception as e:
                results.append({"error": str(e), "docPath": doc_path})
        
        return {"documents": results, "totalMatches": total_matches}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def search_knowledge_base(
    query: str = Field(description="自然语言搜索查询，例如 '如何集成环信 IM' 或 'login error'"),
    doc_type: str = Field(default=None, description="可选，过滤文档类型: 'sdk', 'uikit', 'callkit'"),
    platform: str = Field(default=None, description="可选，过滤平台: 'android', 'ios' 等")
) -> List[Dict[str, Any]]:
    """
    全文检索知识库 (基于搜索引擎)。
    支持自然语言查询，返回按相关性排序的文档列表，包含匹配高亮摘要。
    推荐在用户提出模糊问题时使用。
    """
    # 异步执行搜索
    results = await asyncio.to_thread(global_indexer.search, query, 10, doc_type, platform)
    return results

def main():
    parser = argparse.ArgumentParser(description="环信文档搜索 MCP 服务")
    parser.add_argument("--transport", "-t", choices=["stdio", "http", "sse"], default="http")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", "-p", type=int, default=443)
    parser.add_argument("--path", default="/mcp/")
    
    args = parser.parse_args()
    
    # 初始化索引 (在启动时)
    # 只能在事件循环中运行 async 函数，但 mcp.run 会接管事件循环
    # 所以我们在 main 中先运行一次索引构建（同步阻塞方式，或者 fire-and-forget）
    # 为了简单起见，我们使用 asyncio.run 来执行索引构建，然后再启动 MCP
    
    print("正在初始化搜索引擎...")
    try:
        asyncio.run(build_index_async(DOC_ROOT, UIKIT_ROOT, CALLKIT_ROOT))
    except Exception as e:
        print(f"索引构建失败: {e}")
        print("服务将继续运行，但搜索功能可能不可用。")
    
    print(f"启动环信文档搜索MCP服务器 (v1.1.0 - Full Text Search)")
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port, path=args.path)
    else:
        mcp.run(transport="http", host=args.host, port=args.port, path=args.path)

if __name__ == "__main__":
    main()
