# 环信文档搜索 MCP 服务

这是一个基于 FastMCP 构建的环信文档搜索服务，用于搜索和检索环信各平台的文档内容。

## 功能特点

- 按平台搜索文档（Android、iOS、Web、Flutter等）
- 获取文档全文内容
- 在文档中搜索关键字并返回上下文
- 支持 HTTP 传输模式，便于远程访问
- 提供 MCP 标准接口，兼容各种 MCP 客户端

## 安装

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 确保 `document` 目录存在于项目根目录中

## 使用方法

### 启动 MCP 服务器

```bash
# 直接运行
python src/server.py

# 或者使用项目脚本
easemob-doc-mcp
```

服务器将在 `http://0.0.0.0:9000` 上运行，提供 HTTP 传输模式的 MCP 服务。

### 服务器配置

当前服务器配置：
- **传输模式**: HTTP
- **主机**: 0.0.0.0（绑定所有网络接口）
- **端口**: 9000
- **日志级别**: DEBUG
- **MCP 端点**: http://127.0.0.1:9000/mcp/

## 在 Cursor 中配置 MCP 客户端

### 方法一：HTTP 传输模式（推荐）

在 Cursor 的 MCP 配置文件中添加：

```json
{
  "mcpServers": {
    "easemob-doc-mcp": {
      "transport": "http",
      "url": "http://127.0.0.1:9000/mcp/"
    }
  }
}
```

### 方法二：命令行传输模式

```json
{
  "mcpServers": {
    "easemob-doc-mcp": {
      "command": "python",
      "args": ["src/server.py"],
      "env": {},
      "description": "环信文档搜索服务 - 按平台搜索文档并获取内容"
    }
  }
}
```

## 可用的 MCP 工具

### 1. search_platform_docs

搜索特定平台的文档目录

**参数:**
- `platform` (string): 平台名称，如 'android', 'ios', 'web', 'flutter' 等

**返回:**
- 匹配的文档路径列表

**示例:**
```python
# 搜索Android平台文档
docs = await mcp.call("search_platform_docs", {"platform": "android"})

# 搜索iOS平台文档
docs = await mcp.call("search_platform_docs", {"platform": "ios"})
```

### 2. get_document_content

获取文档内容，并根据关键字搜索相关内容

**参数:**
- `doc_path` (string): 文档相对路径
- `keyword` (string, 可选): 搜索关键字

**返回:**
- 包含文档内容和匹配片段的字典

**示例:**
```python
# 获取文档全文内容
content = await mcp.call("get_document_content", {
    "doc_path": "android/initialization.md"
})

# 在文档中搜索关键字
results = await mcp.call("get_document_content", {
    "doc_path": "android/initialization.md", 
    "keyword": "初始化"
})
```

## 支持的文档平台

- **Android**: Android SDK 文档
- **iOS**: iOS SDK 文档  
- **Web**: Web SDK 文档
- **Flutter**: Flutter SDK 文档
- **React Native**: React Native SDK 文档
- **Unity**: Unity SDK 文档
- **Electron**: Electron SDK 文档
- **HarmonyOS**: HarmonyOS SDK 文档
- **Applet**: 小程序 SDK 文档
- **Server-side**: 服务端文档
- **Linux**: Linux SDK 文档
- **Windows**: Windows SDK 文档

## 使用示例

### 在 Cursor 中使用

1. 启动服务器：
   ```bash
   python src/server.py
   ```

2. 在 Cursor 中配置 MCP 客户端（使用上面的配置）

3. 在 Cursor 中直接使用：
   ```
   请帮我搜索Android平台的初始化相关文档
   ```

### 编程方式使用

```python
from fastmcp import FastMCPClient

# 创建客户端
client = FastMCPClient("http://127.0.0.1:9000")

# 搜索文档
android_docs = await client.search_platform_docs(platform="android")

# 获取文档内容
content = await client.get_document_content(
    doc_path="android/initialization.md",
    keyword="初始化"
)
```

## 服务器日志

启动服务器后，你会看到类似以下的日志：

```
启动环信文档搜索MCP服务器
[07/31/25 15:03:08] INFO     Starting MCP server 'FastMCP' with transport 'http' on http://0.0.0.0:9000/mcp/
INFO:     Started server process [92779]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
```

## 故障排除

### 常见问题

1. **端口被占用**: 如果9000端口被占用，可以修改 `src/server.py` 中的端口配置
2. **连接失败**: 确保服务器正在运行，并且防火墙允许9000端口访问
3. **文档路径错误**: 确保 `document` 目录存在且包含正确的文档结构

### 调试模式

服务器默认运行在 DEBUG 模式下，会显示详细的请求日志，包括：
- HTTP 请求和响应
- MCP 协议消息
- 错误信息

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
├── requirements.txt      # 依赖列表
└── README.md            # 项目说明
```

## 开发

### 添加新的工具

在 `src/server.py` 中添加新的 `@mcp.tool()` 装饰器函数即可。

### 修改服务器配置

编辑 `src/server.py` 中的 `main()` 函数来修改服务器配置。

## 许可证

本项目遵循 MIT 许可证。 