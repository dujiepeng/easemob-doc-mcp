# 文档搜索服务

这是一个使用 Python FastMCP 和 FastAPI 构建的文档搜索服务，用于搜索和检索文档内容。

## 功能特点

- 按平台搜索文档
- 获取文档全文内容
- 在文档中搜索关键字并返回上下文
- 同时支持 FastAPI 和 FastMCP 接口

## 安装

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 确保 `document` 目录存在于项目根目录中

## 使用方法

### 运行模式

本服务支持三种运行模式：

1. **FastAPI 模式**（默认）：提供 REST API 接口
2. **FastMCP 模式**：提供 FastMCP 接口，用于 Cursor 等工具
3. **双模式**：同时运行 FastAPI 和 FastMCP

### 运行 FastAPI 服务器

```bash
cd fastmcp_server
python main.py --mode api
```

或者简单地：

```bash
cd fastmcp_server
python main.py
```

服务器将在 `http://localhost:8000` 上运行。

### 运行 FastMCP 服务器

```bash
cd fastmcp_server
python main.py --mode mcp
```

或者使用专门的 MCP 脚本：

```bash
cd fastmcp_server
python run_mcp.py
```

### 同时运行两种服务器

```bash
cd fastmcp_server
python main.py --mode both
```

## FastAPI 端点

- `GET /api/search-docs?platform={platform}` - 搜索指定平台的文档
- `GET /api/get-doc-content?path={path}&keyword={keyword}` - 获取文档内容和关键字搜索结果

## 在 Cursor 中配置 FastMCP

1. 确保 FastMCP 服务器正在运行：
   ```bash
   cd fastmcp_server
   python run_mcp.py
   ```

2. 在 Cursor 中配置 MCP：

```
    "docs-search": {
          "command": "python",
          "args": ["/Users/dujiepeng/Desktop/easemob_docs_mcp/fastmcp_server/run_mcp.py"],
          "env": {},
          "description": "环信文档搜索服务 - 按平台搜索文档并获取内容"
    }
```

1. 使用示例：
   ```python
   # 搜索Android平台文档
   docs = await mcp.call("search_platform_docs", {"platform": "android"})
   
   # 获取文档内容
   content = await mcp.call("get_document_content", {"doc_path": "android/overview.md"})
   
   # 在文档中搜索关键字
   results = await mcp.call("get_document_content", {
       "doc_path": "android/overview.md", 
       "keyword": "初始化"
   })
   ```

## FastAPI 文档

启动服务后，可以访问以下网址查看交互式 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 示例运行

运行示例客户端：

```bash
cd fastmcp_server
python client_example.py
``` 