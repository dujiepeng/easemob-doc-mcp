# 环信文档搜索服务

这是一个基于 Python FastMCP 和 FastAPI 构建的文档搜索服务，支持多平台文档搜索和 SSE 流式响应。现在可以作为 npm 包使用！

## ✨ 功能特点

- 🔍 按平台搜索文档（Android、iOS、Web、Flutter等）
- 📄 获取文档全文内容
- 🔎 在文档中搜索关键字并返回上下文
- 🌊 支持 SSE（Server-Sent Events）流式响应
- 🚀 同时支持 FastAPI 和 FastMCP 接口
- 📦 可作为 npm 包使用
- 🖥️ 提供命令行工具

## 📦 作为 npm 包使用

### 安装

```bash
npm install easemob-doc-search
```

### 基本使用

```javascript
const EasemobDocSearchClient = require('easemob-doc-search');

// 创建客户端
const client = new EasemobDocSearchClient({
  baseUrl: 'http://localhost:8000'
});

// 搜索文档
const result = await client.searchDocs('android');
console.log(`找到 ${result.results.length} 个文档`);

// 获取文档内容
const content = await client.getDocContent('android/overview.md', '初始化');
console.log(`文档长度: ${content.content?.length} 字符`);
```

### SSE 流式使用

```javascript
// 流式搜索文档
const stream = client.searchDocsStream('android');
for await (const event of stream) {
  switch (event.type) {
    case 'start':
      console.log(`📡 ${event.message}`);
      break;
    case 'progress':
      console.log(`📊 ${event.message}`);
      break;
    case 'results_batch':
      console.log(`📄 批次 ${event.batch}/${event.total_batches}:`);
      event.data?.forEach(doc => console.log(`   - ${doc}`));
      break;
    case 'complete':
      console.log(`✅ 搜索完成，共找到 ${event.total_results} 个文档`);
      break;
  }
}

// 流式获取文档内容
const contentStream = client.getDocContentStream('android/overview.md', '初始化');
for await (const event of contentStream) {
  switch (event.type) {
    case 'doc_info':
      console.log(`📄 文档: ${event.docPath}, 长度: ${event.content_length} 字符`);
      break;
    case 'match':
      console.log(`📍 匹配 ${event.match_index}/${event.total_matches}: ${event.data.line}`);
      break;
  }
}
```

## 🖥️ 命令行工具

### 安装全局命令

```bash
npm install -g easemob-doc-search
```

### 使用命令

```bash
# 健康检查
easemob-doc-search health

# 搜索文档
easemob-doc-search search android

# 流式搜索
easemob-doc-search search android --stream

# 获取文档内容
easemob-doc-search content android/overview.md

# 搜索文档内容
easemob-doc-search content android/overview.md --keyword 初始化

# 流式获取内容
easemob-doc-search content android/overview.md --keyword 初始化 --stream

# 启动服务器
easemob-doc-search serve --port 8000 --mode api
```

## 🚀 本地开发

### 安装依赖

1. 安装 Node.js 依赖：
```bash
npm install
```

2. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```

3. 构建 TypeScript：
```bash
npm run build
```

### 运行模式

本服务支持三种运行模式：

1. **FastAPI 模式**（默认）：提供 REST API 和 SSE 接口
2. **FastMCP 模式**：提供 FastMCP 接口，用于 Cursor 等工具
3. **双模式**：同时运行 FastAPI 和 FastMCP

### 启动服务器

```bash
# FastAPI 模式
cd fastmcp_server
python main.py --mode api

# 或者使用 npm 命令
npm run start serve --mode api
```

服务器将在 `http://localhost:8000` 上运行。

## 📡 API 端点

### REST API

- `GET /api/search-docs?platform={platform}` - 搜索指定平台的文档
- `GET /api/get-doc-content?path={path}&keyword={keyword}` - 获取文档内容和关键字搜索结果
- `GET /health` - 健康检查

### SSE 端点

- `GET /api/sse/search-docs?platform={platform}` - 流式搜索文档
- `GET /api/sse/get-doc-content?path={path}&keyword={keyword}` - 流式获取文档内容

## 🔧 在 Cursor 中配置 FastMCP

1. 确保 FastMCP 服务器正在运行：
   ```bash
   cd fastmcp_server
   python run_mcp.py
   ```

2. 在 Cursor 中配置 MCP：

```json
{
  "docs-search": {
    "command": "python",
    "args": ["/path/to/easemob-doc-search/fastmcp_server/run_mcp.py"],
    "env": {},
    "description": "环信文档搜索服务 - 按平台搜索文档并获取内容"
  }
}
```

3. 使用示例：
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

## 📚 示例

查看 `examples/` 目录中的完整示例：

- `basic-usage.js` - 基本使用示例
- `sse-streaming.js` - SSE 流式使用示例

## 📄 FastAPI 文档

启动服务后，可以访问以下网址查看交互式 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🏗️ 项目结构

```
easemob-doc-search/
├── src/                    # TypeScript 源码
│   ├── index.ts           # 主入口文件
│   ├── client.ts          # 客户端类
│   ├── types.ts           # 类型定义
│   └── cli.ts             # 命令行工具
├── dist/                  # 编译后的 JavaScript
├── fastmcp_server/        # Python 服务器
│   ├── main.py           # 主服务器文件
│   └── run_mcp.py        # MCP 服务器
├── examples/              # 使用示例
├── document/              # 文档目录
├── package.json           # npm 包配置
├── tsconfig.json          # TypeScript 配置
└── requirements.txt       # Python 依赖
```

## 📦 发布到 npm

```bash
# 构建项目
npm run build

# 发布到 npm
npm publish
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## �� 许可证

MIT License 