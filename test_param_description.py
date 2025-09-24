#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入server.py中的函数
from src.server import search_platform_docs, get_document_content

def main():
    """测试参数描述"""
    print("搜索平台文档工具参数信息:")
    
    # 获取search_platform_docs的参数信息
    if hasattr(search_platform_docs, 'parameters'):
        params = search_platform_docs.parameters
        print(json.dumps(params, indent=2, ensure_ascii=False))
    else:
        print("无法获取参数信息")
    
    print("\n获取文档内容工具参数信息:")
    
    # 获取get_document_content的参数信息
    if hasattr(get_document_content, 'parameters'):
        params = get_document_content.parameters
        print(json.dumps(params, indent=2, ensure_ascii=False))
    else:
        print("无法获取参数信息")

if __name__ == "__main__":
    main()
