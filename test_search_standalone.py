#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, List

# 文档根目录
DOC_ROOT = Path(__file__).parent / "document"
# UIKit文档目录
UIKIT_ROOT = Path(__file__).parent / "uikit"

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
            "rest": "server-sid
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
