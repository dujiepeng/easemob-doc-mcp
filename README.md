# 环信文档搜索 MCP 服务

这是一个基于 FastMCP 构建的环信文档搜索服务，用于搜索和检索环信各平台的技术文档。

## 功能特点

- 按平台搜索文档（Android、iOS、Web、Flutter、React Native等）
- 获取文档全文内容
- 在文档中搜索关键字并返回上下文
- 支持 MCP 协议，可与 Cursor 等工具集成

## 安装

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 确保 `document` 目录存在于项目根目录中

## 使用方法

### 启动 MCP 服务器

```bash
python src/server.py
```

服务器将在 `http://0.0.0.0:9000` 上运行，提供 MCP 服务。

### 在 Cursor 中配置

1. 确保 MCP 服务器正在运行：
   ```bash
   python src/server.py
   ```

2. 在 Cursor 的 MCP 配置中添加：

```json
{
  "easemob-doc-mcp": {
    "transport": "http",
    "url": "http://127.0.0.1:9000/mcp/"
  }
}
```

## 可用的 MCP 工具

### 1. search_platform_docs

搜索特定平台的文档目录

**参数：**
- `platform` (string): 平台名称，如 'android', 'ios', 'web', 'flutter' 等

**返回：**
- 匹配的文档路径列表

**示例：**
```python
# 搜索Android平台文档
docs = await mcp.call("search_platform_docs", {"platform": "android"})
```

### 2. get_document_content

获取文档内容，并根据关键字搜索相关内容

**参数：**
- `doc_path` (string): 文档相对路径
- `keyword` (string, 可选): 搜索关键字

**返回：**
- 包含文档内容和匹配片段的字典

**示例：**
```python
# 获取文档内容
content = await mcp.call("get_document_content", {
    "doc_path": "android/initialization.md"
})

# 在文档中搜索关键字
results = await mcp.call("get_document_content", {
    "doc_path": "android/initialization.md", 
    "keyword": "初始化"
})
```

## 支持的平台

- Android
- iOS  
- Web
- Flutter
- React Native
- Unity
- Electron
- HarmonyOS
- 小程序（微信、支付宝、百度、字节跳动、QQ）
- Linux
- Windows
- 服务端

## 项目结构

```
easemob-doc-mcp/
├── src/
│   └── server.py          # MCP服务器主文件
├── document/              # 文档根目录
│   ├── android/           # Android文档
│   ├── ios/              # iOS文档
│   ├── web/              # Web文档
│   └── ...               # 其他平台文档
├── pyproject.toml        # 项目配置
└── requirements.txt      # 依赖列表
```

## 开发

### 安装开发依赖

```bash
pip install -e .
```

### 运行测试

```bash
python src/server.py
```

服务器启动后，可以通过 MCP 客户端进行测试。 