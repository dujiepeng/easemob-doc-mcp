#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path

def create_callkit_test_files():
    """创建callkit目录结构用于测试"""
    print("创建callkit目录结构用于测试...")
    
    # 创建callkit目录
    callkit_dir = Path(__file__).parent / "callkit"
    callkit_dir.mkdir(exist_ok=True)
    print(f"已创建callkit目录: {callkit_dir}")
    
    # 创建android子目录
    android_dir = callkit_dir / "android"
    android_dir.mkdir(exist_ok=True)
    print(f"已创建android子目录: {android_dir}")
    
    # 创建ios子目录
    ios_dir = callkit_dir / "ios"
    ios_dir.mkdir(exist_ok=True)
    print(f"已创建ios子目录: {ios_dir}")
    
    # 创建web子目录
    web_dir = callkit_dir / "web"
    web_dir.mkdir(exist_ok=True)
    print(f"已创建web子目录: {web_dir}")
    
    # 创建测试文件 - Android
    test_file_android = android_dir / "quickstart.md"
    with open(test_file_android, "w", encoding="utf-8") as f:
        f.write("# CallKit Android 快速开始\n\n这是CallKit Android的快速开始指南。")
    print(f"已创建Android测试文件: {test_file_android}")
    
    # 创建测试文件 - iOS
    test_file_ios = ios_dir / "quickstart.md"
    with open(test_file_ios, "w", encoding="utf-8") as f:
        f.write("# CallKit iOS 快速开始\n\n这是CallKit iOS的快速开始指南。")
    print(f"已创建iOS测试文件: {test_file_ios}")
    
    # 创建测试文件 - Web
    test_file_web = web_dir / "quickstart.md"
    with open(test_file_web, "w", encoding="utf-8") as f:
        f.write("# CallKit Web 快速开始\n\n这是CallKit Web的快速开始指南。")
    print(f"已创建Web测试文件: {test_file_web}")
    
    # 创建README文件
    readme_file = callkit_dir / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write("# CallKit 文档\n\n环信CallKit文档目录，包含Android、iOS和Web平台的文档。")
    print(f"已创建README文件: {readme_file}")
    
    print("\n测试文件创建完成！")

if __name__ == "__main__":
    create_callkit_test_files()
