# 环信文档搜索 MCP 服务 API 参考

这是一个基于FastMCP框架开发的环信文档搜索服务，主要用于帮助用户快速查找和获取环信SDK、UIKit和CallKit相关的文档内容。

## 主要功能

服务提供两个核心工具函数：

1. `search_platform_docs` - 搜索特定平台的文档目录
2. `get_document_content` - 获取文档内容并支持关键词搜索

## 工具函数详解

### search_platform_docs

**功能**：搜索特定平台的文档目录

**参数**：
- `doc_type`：文档类型（必填）
  - `sdk`：搜索document目录下的文档
  - `uikit`：搜索uikit目录下的文档
  - `callkit`：搜索callkit目录下的文档
- `platform`：平台名称（可选）
  - 支持android、ios、web、flutter、react-native等
  - 支持部分匹配和常用词语映射（如"小程序"→"applet"）

**返回内容**：
```json
{
    "documents": ["android/quickstart.md", "android/integration.md", ...],
    "platform": "android",
    "count": 42,
    "error": null
}
```

### get_document_content

**功能**：获取文档内容，支持关键词搜索

**参数**：
- `doc_paths`：文档相对路径列表
- `keyword`：搜索关键词（可选）

**返回内容**：
```json
{
    "documents": [
        {
            "content": "文档完整内容",
            "docPath": "android/quickstart.md",
            "matches": [
                {
                    "lineNumber": 10,
                    "context": "包含前后各2行的上下文",
                    "line": "匹配行的内容"
                }
            ],
            "error": null
        }
    ],
    "totalMatches": 5,
    "error": null
}
```

## 与AI交互流程

1. **搜索文档**：
   - AI通过调用`search_platform_docs`搜索特定平台的文档
   - 用户可以指定文档类型和平台名称

2. **获取文档内容**：
   - 根据搜索结果，AI调用`get_document_content`获取具体文档内容
   - 可以指定关键词进行内容过滤

3. **内容解析与回答**：
   - AI解析文档内容，提取相关信息
   - 根据用户问题，提供准确的答案和引导

## 完整使用流程

1. 用户提出关于环信SDK、UIKit或CallKit的问题
2. AI调用`search_platform_docs`找到相关平台的文档
3. AI调用`get_document_content`获取文档内容，可指定关键词
4. AI分析文档内容，提取相关信息回答用户问题
5. 如需深入了解，AI可继续搜索其他相关文档

服务支持HTTP、SSE和stdio三种传输协议，默认使用HTTP协议，监听0.0.0.0:443，路径为/mcp/。
