#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, List

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 文档根目录
DOC_ROOT = Path(__file__).parent / "document"
# UIKit文档目录
UIKIT_ROOT = Path(__file__).parent / "uikit"

async def get_document_content(doc_paths: List[str] = None, keyword: str = "") -> Dict[str, Any]:
    """
    获取文档内容，并根据关键字搜索相关内容
    
    参数:
    - doc_paths: 文档相对路径列表，例如 ["android/quickstart.md", "uikit/chatuikit/android/chatuikit_quickstart.md"]
                如果提供单个字符串，将自动转换为列表
    - keyword: 搜索关键字（可选），如果提供则会在文档中搜索匹配的内容
    """
    try:
        # 处理输入参数
        if doc_paths is None:
            doc_paths = []
        elif isinstance(doc_paths, str):
            doc_paths = [doc_paths]
        
        # 初始化结果
        results = []
        total_matches = 0
        
        # 处理每个文档路径
        for doc_path in doc_paths:
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
                    results.append({
                        "content": None, 
                        "docPath": doc_path,
                        "matches": [],
                        "error": "文档不存在"
                    })
                    continue
                
                # 读取文件内容
                with open(fullPath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 初始化当前文档的匹配结果
                matches = []
                
                # 如果有关键字，进行搜索
                if keyword and keyword.strip() != "":
                    lines = content.split('\n')
                    
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
                
                # 添加当前文档的结果
                results.append({
                    "content": content,
                    "docPath": doc_path,
                    "matches": matches,
                    "error": None
                })
                
                # 更新总匹配数
                total_matches += len(matches)
                
            except Exception as e:
                error_msg = f"获取文档 {doc_path} 内容失败: {str(e)}"
                print(f"获取文档内容错误: {str(e)}")
                results.append({
                    "content": None, 
                    "docPath": doc_path,
                    "matches": [],
                    "error": error_msg
                })
        
        # 返回所有文档的结果
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

async def test_document_content():
    """测试多文档路径检索功能"""
    # 测试1：单个文档路径
    print("===== 测试1：单个文档路径 =====")
    result = await get_document_content("android/quickstart.md")
    print(f"文档数量: {len(result['documents'])}")
    print(f"总匹配数: {result['totalMatches']}")
    print(f"错误: {result['error']}")
    
    # 打印第一个文档的部分内容
    if result['documents']:
        doc = result['documents'][0]
        print(f"文档路径: {doc['docPath']}")
        print(f"文档内容前100个字符: {doc['content'][:100] if doc['content'] else 'None'}")
        print(f"匹配数: {len(doc['matches'])}")
        print(f"错误: {doc['error']}")
    
    # 测试2：多个文档路径
    print("\n===== 测试2：多个文档路径 =====")
    result = await get_document_content([
        "android/quickstart.md", 
        "android/initialization.md",
        "uikit/chatuikit/android/chatuikit_quickstart.md"
    ])
    print(f"文档数量: {len(result['documents'])}")
    print(f"总匹配数: {result['totalMatches']}")
    print(f"错误: {result['error']}")
    
    # 打印每个文档的基本信息
    for i, doc in enumerate(result['documents']):
        print(f"\n文档{i+1}: {doc['docPath']}")
        print(f"内容长度: {len(doc['content']) if doc['content'] else 0}")
        print(f"匹配数: {len(doc['matches'])}")
        print(f"错误: {doc['error']}")
    
    # 测试3：带关键字的搜索
    print("\n===== 测试3：带关键字的搜索 =====")
    result = await get_document_content([
        "android/quickstart.md", 
        "android/initialization.md"
    ], "初始化")
    print(f"文档数量: {len(result['documents'])}")
    print(f"总匹配数: {result['totalMatches']}")
    print(f"错误: {result['error']}")
    
    # 打印每个文档的匹配结果
    for i, doc in enumerate(result['documents']):
        print(f"\n文档{i+1}: {doc['docPath']}")
        print(f"匹配数: {len(doc['matches'])}")
        
        # 打印前3个匹配结果
        for j, match in enumerate(doc['matches'][:3]):
            print(f"\n匹配{j+1}:")
            print(f"行号: {match['lineNumber']}")
            print(f"行内容: {match['line']}")
            print(f"上下文: \n{match['context']}")
        
        if len(doc['matches']) > 3:
            print(f"... 还有 {len(doc['matches']) - 3} 个匹配结果")
    
    # 测试4：不存在的文档
    print("\n===== 测试4：不存在的文档 =====")
    result = await get_document_content(["nonexistent.md", "android/quickstart.md"])
    print(f"文档数量: {len(result['documents'])}")
    print(f"总匹配数: {result['totalMatches']}")
    print(f"错误: {result['error']}")
    
    # 打印每个文档的错误信息
    for i, doc in enumerate(result['documents']):
        print(f"\n文档{i+1}: {doc['docPath']}")
        print(f"错误: {doc['error']}")
        print(f"内容是否存在: {'是' if doc['content'] else '否'}")

if __name__ == "__main__":
    asyncio.run(test_document_content())
