from fastapi import FastAPI, HTTPException, Query
from fastmcp import FastMCP
import os
import glob
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import argparse

# 创建FastAPI应用
app = FastAPI(title="文档搜索服务", description="基于FastMCP的文档搜索服务")
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
            return {"content": None, "error": "文档不存在"}
        
        # 读取文件内容
        with open(fullPath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果没有关键字，返回全部内容
        if not keyword or keyword.strip() == "":
            return {
                "content": content,
                "docPath": doc_path,
                "matches": []
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
            "matches": matches
        }
    except Exception as e:
        print(f"获取文档内容错误: {str(e)}")
        return {"content": None, "error": "获取文档内容失败"}

# API路由到FastAPI
@app.get("/api/search-docs")
async def api_search_docs(platform: str = Query(..., description="平台名称，如android, ios, web等")):
    """搜索特定平台的文档API"""
    results = await search_platform_docs(platform)
    return {"results": results}

@app.get("/api/get-doc-content")
async def api_get_doc_content(
    path: str = Query(..., description="文档相对路径"),
    keyword: str = Query("", description="搜索关键字（可选）")
):
    """获取文档内容API"""
    content = await get_document_content(path, keyword)
    return content

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 主入口点
def run_fastapi_server():
    """运行FastAPI服务器"""
    print("启动FastAPI服务器在 http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_fastmcp_server():
    """运行FastMCP服务器"""
    print("启动FastMCP服务器")
    mcp.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="文档搜索服务")
    parser.add_argument("--mode", choices=["api", "mcp", "both"], default="api", 
                        help="运行模式: api=FastAPI服务器, mcp=FastMCP服务器, both=两者都运行")
    
    args = parser.parse_args()
    
    if args.mode == "api":
        run_fastapi_server()
    elif args.mode == "mcp":
        run_fastmcp_server()
    elif args.mode == "both":
        # 对于同时运行两个服务器，我们需要在单独的进程中运行它们
        import threading
        
        api_thread = threading.Thread(target=run_fastapi_server)
        api_thread.daemon = True
        api_thread.start()
        
        # FastMCP在主线程运行
        run_fastmcp_server() 