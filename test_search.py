#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入server.py中的函数
from src.server import search_platform_docs, get_document_content

async def test_search():
    """测试搜索功能"""
    # 测试搜索UIKit中的Android平台文档
    print("===== 测试搜索UIKit中的Android平台文档 =====")
    result = await search_platform_docs('uikit', 'android')
    print(f"找到 {result['count']} 个文档")
    print(f"平台: {result['platform']}")
    print(f"错误: {result['error']}")
    
    # 打印前5个文档路径
    docs = result['documents']
    for i, doc in enumerate(docs[:5]):
        print(f"{i+1}. {doc}")
    print("...")
    
    # 测试搜索SDK中的Android平台文档
    print("\n===== 测试搜索SDK中的Android平台文档 =====")
    result = await search_platform_docs('sdk', 'android')
    print(f"找到 {result['count']} 个文档")
    print(f"平台: {result['platform']}")
    print(f"错误: {result['error']}")
    
    # 打印前5个文档路径
    docs = result['documents']
    for i, doc in enumerate(docs[:5]):
        print(f"{i+1}. {doc}")
    print("...")
    
    # 测试搜索不存在的平台
    print("\n===== 测试搜索不存在的平台 =====")
    result = await search_platform_docs('uikit', 'nonexistent')
    print(f"找到 {result['count']} 个文档")
    print(f"平台: {result['platform']}")
    print(f"错误: {result['error']}")

if __name__ == "__main__":
    asyncio.run(test_search())
