# -*- coding: utf-8 -*-
from fastmcp import FastMCP
import os
import sys
import argparse
import asyncio
from typing import List, Dict, Any, Union
from pathlib import Path
from pydantic import Field
from functools import lru_cache, wraps
import json
try:
    from .indexer import global_indexer, build_index_async
except ImportError:
    try:
        from src.indexer import global_indexer, build_index_async
    except ImportError:
        from indexer import global_indexer, build_index_async

# 创建FastMCP实例
mcp = FastMCP()

# --- 日志系统 ---
def log_tool_call(func):
    """工具调用日志装饰器，输出到 stderr 以免干扰 stdio 传输"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        tool_name = func.__name__
        # 打印请求
        print(f"\n[Tool Request: {tool_name}]", file=sys.stderr)
        print(f"Args: {json.dumps(kwargs, ensure_ascii=False, indent=2)}", file=sys.stderr)
        
        try:
            result = await func(*args, **kwargs)
            # 打印响应摘要
            print(f"[Tool Response: {tool_name}] Success", file=sys.stderr)
            # 如果结果太长，只打印关键信息
            res_str = json.dumps(result, ensure_ascii=False)
            if len(res_str) > 500:
                print(f"Result (truncated): {res_str[:500]}...", file=sys.stderr)
            else:
                print(f"Result: {res_str}", file=sys.stderr)
            return result
        except Exception as e:
            print(f"[Tool Response: {tool_name}] Failed: {e}", file=sys.stderr)
            raise e
    return wrapper

# 文档仓库配置
DOC_REPO_URL = os.environ.get("DOC_REPO_URL", "https://github.com/easemob/easemob-doc.git")
DOC_REPO_BRANCH = os.environ.get("DOC_REPO_BRANCH", "doc-v2")

# 文档根目录
ROOT_DIR = Path(__file__).parent.parent
DOC_ROOT = ROOT_DIR / "document"
UIKIT_ROOT = ROOT_DIR / "uikit"
CALLKIT_ROOT = ROOT_DIR / "callkit"
TEMP_DIR = Path("/tmp/temp_docs")  # 使用 /tmp 避免 Docker 挂卷时的权限问题

async def sync_all_docs(force_index: bool = False):
    """同步所有文档 (通过下载 zip 压缩包实现，更轻快)"""
    import shutil
    import zipfile
    import urllib.request
    import io

    print(f"🚀 开始同步文档仓库 (Archive Mode)...", file=sys.stderr)
    
    # 1. 清理并创建临时目录
    if TEMP_DIR.exists():
        await asyncio.to_thread(shutil.rmtree, str(TEMP_DIR))
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        # 2. 下载 ZIP 压缩包
        # GitHub Archive URL 格式: https://github.com/user/repo/archive/refs/heads/branch.zip
        repo_base = DOC_REPO_URL.replace(".git", "")
        zip_url = f"{repo_base}/archive/refs/heads/{DOC_REPO_BRANCH}.zip"
        
        print(f"📥 Downloading: {zip_url}", file=sys.stderr)
        
        def _download_and_extract():
            with urllib.request.urlopen(zip_url) as response:
                with zipfile.ZipFile(io.BytesIO(response.read())) as z:
                    z.extractall(str(TEMP_DIR))
            
            # 获取解压后的顶级目录名 (通常是 repo-branch)
            top_dirs = [d for d in os.listdir(TEMP_DIR) if os.path.isdir(TEMP_DIR / d)]
            if not top_dirs:
                raise Exception("ZIP 解压后未找到目录")
            return TEMP_DIR / top_dirs[0]

        extracted_root = await asyncio.to_thread(_download_and_extract)
        print(f"✅ Extracted to: {extracted_root.name}", file=sys.stderr)

        # 3. 复制子目录
        subfolders = {
            "docs/document": DOC_ROOT,
            "docs/uikit": UIKIT_ROOT,
            "docs/callkit": CALLKIT_ROOT
        }
        
        any_updated = force_index
        for src_rel, dest_path in subfolders.items():
            src_path = extracted_root / src_rel
            if src_path.exists():
                print(f"📂 Updating {dest_path.name}...", file=sys.stderr)
                if dest_path.exists():
                    await asyncio.to_thread(shutil.rmtree, str(dest_path))
                await asyncio.to_thread(shutil.copytree, str(src_path), str(dest_path))
                any_updated = True
            else:
                print(f"⚠️ Warning: {src_rel} 不存在于源代码中", file=sys.stderr)
        
        # 4. 如果有更新，重建索引并清理缓存
        if any_updated:
            print("🔍 文档有变动或强制更新，重建索引并清理缓存...", file=sys.stderr)
            _scan_directory_docs.cache_clear()
            await build_index_async(DOC_ROOT, UIKIT_ROOT, CALLKIT_ROOT, rebuild=True)
        else:
            print("✨ 文档无变动，跳过索引重建。", file=sys.stderr)
            
    except Exception as e:
        print(f"❌ 同步过程中出错: {e}", file=sys.stderr)
    finally:
        # 5. 清理临时目录
        if TEMP_DIR.exists():
            await asyncio.to_thread(shutil.rmtree, str(TEMP_DIR))

async def ensure_docs_ready():
    """启动时检查文档是否就绪，若缺失则立即同步"""
    print("📋 检查本地文档完整性...", file=sys.stderr)
    folders = [DOC_ROOT, UIKIT_ROOT, CALLKIT_ROOT]
    missing = any(not (f.exists() and f.is_dir() and any(f.iterdir())) for f in folders)
    
    if missing:
        print("⚠️ 检测到关键文档缺失，正在启动紧急同步...", file=sys.stderr)
        await sync_all_docs(force_index=True)
    else:
        print("✅ 本地文档已就绪。", file=sys.stderr)
        # 即使文档在，也要确保索引存在
        from indexer import exists_in
        if not exists_in(global_indexer.index_dir):
            print("🔍 索引缺失，正在后台构建索引...", file=sys.stderr)
            await build_index_async(DOC_ROOT, UIKIT_ROOT, CALLKIT_ROOT, rebuild=True)

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
@log_tool_call
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
@log_tool_call
async def get_document_content(
    doc_paths: Union[str, List[str]] = Field(
        default=None,
        description="文档相对路径列表，例如 [\"sdk/android/quickstart.md\", \"uikit/chatuikit/android/chatuikit_quickstart.md\"]，或者单个字符串路径"
    ),
    keyword: str = Field(
        default="",
        description="可选，用于在返回的文档内容中进行关键词定位（返回上下文）"
    )
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
                elif doc_path.startswith("sdk/"):
                    full_path = DOC_ROOT / doc_path[4:]
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

# @mcp.tool()
# @log_tool_call
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
    parser.add_argument("--path", default="/sse")
    
    args = parser.parse_args()
    
    # 初始化索引 (在启动时)
    # 只能在事件循环中运行 async 函数，但 mcp.run 会接管事件循环
    # 所以我们在 main 中先运行一次索引构建（同步阻塞方式，或者 fire-and-forget）
    # 为了简单起见，我们使用 asyncio.run 来执行索引构建，然后再启动 MCP
    
    print("正在加载环信文档 MCP 服务...", file=sys.stderr)
    try:
        # 1. 启动检查：确保文档存且已建立索引
        asyncio.run(ensure_docs_ready())
        
        # 启动后台定时更新任务
        async def scheduled_update():
            while True:
                # 每天更新一次 (24 * 3600 秒)
                # 为了便于测试，可以通过环境变量设置间隔，默认 86400 秒
                try:
                    update_interval = int(os.environ.get("DOC_UPDATE_INTERVAL_SECONDS", 86400))
                    print(f"下次文档更新将在 {update_interval} 秒后执行...", file=sys.stderr)
                    await asyncio.sleep(update_interval)
                    
                    print("⏰ 开始执行定时更新...", file=sys.stderr)
                    # 执行全量更新
                    await sync_all_docs()
                        
                except Exception as e:
                    print(f"定时更新任务出错: {e}", file=sys.stderr)
                    await asyncio.sleep(60) # 出错后等待 1 分钟重试

        # 在后台启动任务，不阻塞主线程
        import threading
        def run_schedule():
            asyncio.run(scheduled_update())
        
        # 注意: mcp.run() 是阻塞的，所以这里用简单的线程或者在 mcp 内部机制中启动
        # FastMCP 目前可以直接运行，我们把 asyncio task 放到事件循环里最好
        # 但由于 mcp.run() 会接管循环，我们这里用一个简化的方式：
        # 创建一个线程来运行这个独立的 loop (虽然不是最佳实践，但对简单任务有效)
        # 或者，如果 FastMCP 暴露了 startup hook 更好。
        # 鉴于 FastMCP 封装较深，我们简单地用 threading 启动这个 loop
        t = threading.Thread(target=run_schedule, daemon=True)
        t.start()
        
    except Exception as e:
        print(f"索引构建失败: {e}", file=sys.stderr)
        print("服务将继续运行，但搜索功能可能不可用。", file=sys.stderr)
    
    print(f"启动环信文档搜索MCP服务器 (v1.1.11 - Full Text Search)", file=sys.stderr)
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port, path=args.path)
    else:
        mcp.run(transport="http", host=args.host, port=args.port, path=args.path)

if __name__ == "__main__":
    main()
