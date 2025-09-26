import os
from typing import List, Dict, Any
from pathlib import Path

# 文档根目录
DOC_ROOT = Path(__file__).parent.parent / "document"
# UIKit文档目录
UIKIT_ROOT = Path(__file__).parent.parent / "uikit"
# CallKit文档目录
CALLKIT_ROOT = Path(__file__).parent.parent / "callkit"

def search_platform_docs(
    doc_type: str,
    platform: str
) -> Dict[str, Any]:
    """
    搜索特定平台的文档目录
    
    参数:
    - doc_type: 文档类型，必填参数，可选值为 'sdk'、'uikit' 或 'callkit'。
              'sdk': 搜索 document 目录下的文档
              'uikit': 搜索 uikit 目录下的文档
              'callkit': 搜索 callkit 目录下的文档
    - platform: 平台名称，如 'android', 'ios', 'web', 'flutter', 'react-native', 'applet', 'server-side', 'uikit' 等。
              支持部分匹配，例如输入 'and' 会匹配 'android'。
              支持常用词语映射：'小程序' -> 'applet', '鸿蒙' -> 'harmonyos', 'rn' -> 'react-native', 'rest' -> 'server-side'
              
              当指定平台时，将只返回该平台的文档。例如：
              - 当 doc_type='uikit' 且 platform='android' 时，只返回 uikit 下 android 目录中的文档
              - 当 doc_type='sdk' 且 platform='ios' 时，只返回 document/ios 目录下的文档
    
    返回:
    {
        "documents": [            # 文档路径列表
            "android/quickstart.md",
            "android/integration.md",
            ...
        ],
        "platform": "android",    # 匹配的平台名称
        "count": 42,             # 找到的文档数量
        "error": null            # 错误信息，成功时为null
    }
    
    如果没有找到匹配的平台或发生错误，则返回:
    {
        "documents": [],
        "platform": "输入的平台名",
        "count": 0,
        "error": "错误信息或未找到匹配平台"
    }
    """
    try:
        # 验证doc_type参数
        if doc_type.lower() not in ["sdk", "uikit", "callkit"]:
            return {
                "documents": [],
                "platform": platform,
                "count": 0,
                "error": f"无效的文档类型: {doc_type}，必须为 'sdk'、'uikit' 或 'callkit'"
            }
            
        # 确保平台名是小写的，以便统一比较
        lowercasePlatform = platform.lower()
        doc_type = doc_type.lower()
        
        # 平台名称映射字典 - 根据文档类型选择不同的映射
        if doc_type == "uikit":
            # UIKit 特定映射
            platform_mapping = {
                "小程序": "applet",
                "uni-app": "uniapp",  # UIKit中uni-app映射为uniapp
                "鸿蒙": "harmonyos",
                "rn": "react-native",
                "rest": "server-side"
            }
        else:
            # SDK和CallKit的映射
            platform_mapping = {
                "小程序": "applet",
                "uni-app": "applet",
                "鸿蒙": "harmonyos",
                "rn": "react-native",
                "rest": "server-side"
            }
        
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
                            # 例如：chatuikit/android/xxx.md 中的 "android" 是否匹配指定的平台
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
        
        # 如果是搜索CallKit文档
        elif doc_type == "callkit":
            if os.path.exists(CALLKIT_ROOT) and os.path.isdir(CALLKIT_ROOT):
                callkitDirs = []
                # 获取callkit下的所有子目录
                for item in os.listdir(CALLKIT_ROOT):
                    itemPath = os.path.join(CALLKIT_ROOT, item)
                    if os.path.isdir(itemPath):
                        callkitDirs.append(item)
                
                # 检查是否有匹配的callkit子目录
                matchedCallkitDirs = []
                if not platform:  # 如果没有指定平台，则包含所有callkit目录
                    matchedCallkitDirs = callkitDirs
                    matchedPlatforms.append("callkit")
                else:
                    # 检查callkit子目录下是否有与platform匹配的平台目录
                    for callkitDir in callkitDirs:
                        if lowercasePlatform in callkitDir.lower():
                            matchedCallkitDirs.append(callkitDir)
                            if "callkit" not in matchedPlatforms:
                                matchedPlatforms.append("callkit")
                            continue
                            
                        callkitDirPath = os.path.join(CALLKIT_ROOT, callkitDir)
                        # 检查每个callkit子目录下的平台目录
                        if os.path.isdir(callkitDirPath):
                            platformDirs = [d for d in os.listdir(callkitDirPath) if os.path.isdir(os.path.join(callkitDirPath, d))]
                            for platformDir in platformDirs:
                                if lowercasePlatform and lowercasePlatform in platformDir.lower():
                                    matchedCallkitDirs.append(callkitDir)
                                    if "callkit" not in matchedPlatforms:
                                        matchedPlatforms.append("callkit")
                                    break
                
                # 递归获取所有匹配的CallKit的Markdown文件
                for callkitDir in matchedCallkitDirs:
                    callkitDirPath = os.path.join(CALLKIT_ROOT, callkitDir)
                    for root, _, files in os.walk(callkitDirPath):
                        # 检查当前目录是否匹配指定的平台
                        if platform:
                            # 获取相对于callkitDir的路径
                            rel_to_callkit_dir = os.path.relpath(root, callkitDirPath)
                            # 如果不是根目录，检查第一级子目录是否匹配平台名
                            if rel_to_callkit_dir != "." and rel_to_callkit_dir.split(os.sep)[0].lower() != lowercasePlatform:
                                continue
                                
                        for file in files:
                            if file.endswith('.md'):
                                fullPath = os.path.join(root, file)
                                # 转换为相对路径，添加callkit前缀
                                relPath = os.path.relpath(fullPath, CALLKIT_ROOT)
                                results.append(f"callkit/{relPath}")
                
                # 包含callkit根目录下的md文件（如果没有指定平台或者是通用文档）
                if not platform:  # 只有在不指定平台时，才包含根目录下的MD文件
                    for file in os.listdir(CALLKIT_ROOT):
                        if file.endswith('.md'):
                            fullPath = os.path.join(CALLKIT_ROOT, file)
                            relPath = os.path.relpath(fullPath, CALLKIT_ROOT)
                            results.append(f"callkit/{relPath}")
        
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

def get_document_lines(
    doc_path: str,
    line_number: int,
    context_lines: int = 2
) -> Dict[str, Any]:
    """
    获取文档中指定行号及其上下文行的内容
    
    参数:
    - doc_path: 文档相对路径，例如 "android/quickstart.md"
    - line_number: 需要获取的行号（从1开始）
    - context_lines: 需要获取的上下文行数（默认为2）
    
    返回:
    {
        "content": str,          # 获取的内容（包含指定行及其上下文）
        "docPath": str,          # 文档路径
        "startLine": int,        # 返回内容的起始行号
        "endLine": int,          # 返回内容的结束行号
        "totalLines": int,       # 文档总行数
        "error": str or None     # 错误信息，如果成功则为None
    }
    """
    try:
        # 确定文档路径
        if doc_path.startswith("uikit/"):
            # 处理UIKit文档
            relative_path = doc_path[6:]  # 移除 "uikit/" 前缀
            fullPath = os.path.join(UIKIT_ROOT, relative_path)
        elif doc_path.startswith("callkit/"):
            # 处理CallKit文档
            relative_path = doc_path[8:]  # 移除 "callkit/" 前缀
            fullPath = os.path.join(CALLKIT_ROOT, relative_path)
        else:
            # 处理普通文档
            fullPath = os.path.join(DOC_ROOT, doc_path)
        
        # 检查文件是否存在
        if not os.path.exists(fullPath):
            return {
                "content": None,
                "docPath": doc_path,
                "startLine": 0,
                "endLine": 0,
                "totalLines": 0,
                "error": "文档不存在"
            }
        
        # 读取文件内容
        with open(fullPath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 计算文档总行数
        total_lines = len(lines)
        
        # 检查行号是否有效
        if line_number < 1 or line_number > total_lines:
            return {
                "content": None,
                "docPath": doc_path,
                "startLine": 0,
                "endLine": 0,
                "totalLines": total_lines,
                "error": f"行号无效: {line_number}，文档总行数: {total_lines}"
            }
        
        # 计算需要返回的行范围
        start_line = max(1, line_number - context_lines)
        end_line = min(total_lines, line_number + context_lines)
        
        # 获取指定范围的内容
        content_lines = lines[start_line-1:end_line]
        content = ''.join(content_lines)
        
        return {
            "content": content,
            "docPath": doc_path,
            "startLine": start_line,
            "endLine": end_line,
            "totalLines": total_lines,
            "error": None
        }
    except Exception as e:
        error_msg = f"获取文档行内容失败: {str(e)}"
        print(error_msg)
        return {
            "content": None,
            "docPath": doc_path,
            "startLine": 0,
            "endLine": 0,
            "totalLines": 0,
            "error": error_msg
        }

def get_document_content(
    doc_paths: List[str],
    keyword: str = ""
) -> Dict[str, Any]:
    """
    获取文档内容，并根据关键字搜索相关内容
    
    参数:
    - doc_paths: 文档相对路径列表，例如 ["android/quickstart.md", "uikit/chatuikit/android/chatuikit_quickstart.md"]
                如果提供单个字符串，将自动转换为列表
    - keyword: 搜索关键字（可选），如果提供则会在文档中搜索匹配的内容
    
    返回:
    {
        "documents": [           # 文档内容列表
            {
                "content": str or None,  # 文档的完整内容，如果文档不存在或发生错误则为None
                "docPath": str,          # 文档路径
                "matches": [             # 匹配结果列表，如果没有提供关键字或没有匹配则为空列表
                    {
                        "lineNumber": int,  # 匹配行的行号（从1开始）
                        "context": str,     # 匹配行的上下文（包括前后各2行）
                        "line": str         # 匹配的具体行内容
                    },
                    ...
                ],
                "error": str or None     # 错误信息，如果成功则为None
            },
            ...
        ],
        "totalMatches": int,     # 所有文档中匹配的总数
        "error": str or None     # 整体错误信息，如果成功则为None
    }
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
                elif doc_path.startswith("callkit/"):
                    # 处理CallKit文档
                    relative_path = doc_path[8:]  # 移除 "callkit/" 前缀
                    fullPath = os.path.join(CALLKIT_ROOT, relative_path)
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
                
                # 移除制表符，减少返回数据量
                content = content.replace('\t', '')
                
                # 初始化当前文档的匹配结果
                matches = []
                
                # 如果有关键字，进行搜索
                if keyword and keyword.strip() != "":
                    lines = content.split('\n')
                    
                    for i, line in enumerate(lines):
                        # 移除行中的制表符
                        line_no_tabs = line.replace('\t', '')
                        if keyword.lower() in line_no_tabs.lower():
                            # 提取匹配行的上下文（前后各2行）
                            startLine = max(0, i - 2)
                            endLine = min(len(lines) - 1, i + 2)
                            
                            # 确保上下文中也移除了制表符
                            context = '\n'.join([lines[j].replace('\t', '') for j in range(startLine, endLine + 1)])
                            matches.append({
                                "lineNumber": i + 1,
                                "context": context,
                                "line": line_no_tabs
                            })
                
                # 添加当前文档的结果
                if(len(matches) > 0):
                    results.append({
                        # "content": content,
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



def main():
    # 测试搜索文档
    print("===== 测试搜索文档 =====")
    file_paths = search_platform_docs("sdk", "android")
    print(file_paths)
    
    # 如果找到了文档，测试获取文档内容
    if file_paths["count"] > 0:
        # 测试获取文档内容
        print("\n===== 测试获取文档内容 =====")
        doc_path = file_paths["documents"][0]
        print(f"获取文档: {doc_path}")
        content = get_document_content([doc_path], "初始化")
        print(content)
        
        # 测试获取指定行内容
        print("\n===== 测试获取指定行内容 =====")
        line_result = get_document_lines(doc_path, 10, 3)
        print(line_result)

# 主入口点
if __name__ == "__main__":
    main()