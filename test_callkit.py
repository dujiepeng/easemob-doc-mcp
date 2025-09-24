#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入server.py中的函数
from src.server import search_platform_docs, get_document_content

async def test_callkit_support():
    """测试callkit目录的支持"""
    print("===== 测试1：搜索CallKit文档 =====")
    result = await search_platform_docs("callkit")
    print(f"找到 {result['count']} 个文档")
    print(f"平台: {result['platform']}")
    print(f"错误: {result['error']}")
    
    # 打印前5个文档路径
    docs = result['documents']
    if docs:
        print("\n前5个文档路径:")
        for i, doc in enumerate(docs[:5]):
            print(f"{i+1}. {doc}")
        print("...")
    else:
        print("\n未找到文档，创建callkit目录并添加测试文件")
        # 创建callkit目录结构用于测试
        callkit_dir = Path(__file__).parent / "callkit"
        callkit_dir.mkdir(exist_ok=True)
        
        # 创建android子目录
        android_dir = callkit_dir / "android"
        android_dir.mkdir(exist_ok=True)
        
        # 创建测试文件
        test_file = android_dir / "test.md"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("# CallKit Android 测试文件\n\n这是一个测试文件。")
        
        # 创建README文件
        readme_file = callkit_dir / "README.md"
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write("# CallKit 文档\n\n环信CallKit文档目录。")
        
        print(f"已创建测试文件: {test_file}")
        print(f"已创建README文件: {readme_file}")
        
        # 重新搜索
        print("\n重新搜索CallKit文档:")
        result = await search_platform_docs("callkit")
        print(f"找到 {result['count']} 个文档")
        print(f"平台: {result['platform']}")
        
        # 打印文档路径
        docs = result['documents']
        for i, doc in enumerate(docs):
            print(f"{i+1}. {doc}")
    
    print("\n===== 测试2：搜索CallKit Android文档 =====")
    result = await search_platform_docs("callkit", "android")
    print(f"找到 {result['count']} 个文档")
    print(f"平台: {result['platform']}")
    print(f"错误: {result['error']}")
    
    # 打印文档路径
    docs = result['documents']
    for i, doc in enumerate(docs):
        print(f"{i+1}. {doc}")
    
    print("\n===== 测试3：读取CallKit文档内容 =====")
    if docs:
        result = await get_document_content([docs[0]])
        print(f"文档数量: {len(result['documents'])}")
        print(f"总匹配数: {result['totalMatches']}")
        print(f"错误: {result['error']}")
        
        # 打印第一个文档的内容
        if result['documents']:
            doc = result['documents'][0]
            print(f"\n文档路径: {doc['docPath']}")
            print(f"文档内容:\n{doc['content']}")
    else:
        print("没有找到CallKit Android文档，无法测试读取功能")

if __name__ == "__main__":
    asyncio.run(test_callkit_support())
