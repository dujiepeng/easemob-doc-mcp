# 环信文档搜索服务

这是一个基于 **Node.js** 构建的文档搜索服务，支持多平台文档搜索和 SSE 流式响应。现在可以作为 npm 包使用！

## ✨ 功能特点

- 🔍 按平台搜索文档（Android、iOS、Web、Flutter等）
- 📄 获取文档全文内容
- 🔎 在文档中搜索关键字并返回上下文
- 🌊 支持 SSE（Server-Sent Events）流式响应
- 🚀 纯 Node.js 实现，无需 Python 环境
- 📦 可作为 npm 包使用
- 🖥️ 提供命令行工具
- 🔧 支持 MCP（Model Context Protocol）

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

# 获取统计信息
easemob-doc-search stats
```

## 🚀 本地开发

### 环境要求

- Node.js 16+
- npm 或 yarn

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/easemob/easemob-doc-search.git
cd easemob-doc-search

# 2. 安装依赖
npm install

# 3. 构建项目
npm run build

# 4. 启动服务
npm start
```

### 开发模式

```bash
# 开发模式启动（自动重载）
npm run start:dev

# 启动MCP服务器
npm run mcp:dev
```

### 运行模式

本服务支持三种运行模式：

1. **API 模式**（默认）：提供 REST API 和 SSE 接口
2. **MCP 模式**：提供 MCP 接口，用于 Cursor 等工具
3. **双模式**：同时运行 API 和 MCP

### 启动服务器

```bash
# API 模式
npm start

# MCP 模式
npm run mcp

# 或者使用命令行工具
npx easemob-doc-search serve --mode api
```

服务器将在 `http://localhost:8000` 上运行。

## 📡 API 端点

### REST API

- `GET /health` - 健康检查
- `GET /api/search-docs?platform={platform}` - 搜索指定平台的文档
- `GET /api/get-doc-content?path={path}&keyword={keyword}` - 获取文档内容和关键字搜索结果

### SSE 端点

- `GET /api/sse/search-docs?platform={platform}` - 流式搜索文档
- `GET /api/sse/get-doc-content?path={path}&keyword={keyword}` - 流式获取文档内容

## 🔧 在 Cursor 中配置 MCP

1. 确保 MCP 服务器正在运行：
   ```bash
   npm run mcp
   ```

2. 在 Cursor 中配置 MCP：

```json
{
  "docs-search": {
    "command": "node",
    "args": ["/path/to/easemob-doc-search/dist/mcp-server.js"],
    "env": {},
    "description": "环信文档搜索服务 - 按平台搜索文档并获取内容"
  }
}
```

3. 使用示例：
   ```javascript
   // 搜索Android平台文档
   const docs = await mcp.call("search_platform_docs", {"platform": "android"});
   
   // 获取文档内容
   const content = await mcp.call("get_document_content", {"doc_path": "android/overview.md"});
   
   // 在文档中搜索关键字
   const results = await mcp.call("get_document_content", {
       "doc_path": "android/overview.md", 
       "keyword": "初始化"
   });
   ```

## 📚 示例

查看 `examples/` 目录中的完整示例：

- `basic-usage.js` - 基本使用示例
- `sse-streaming.js` - SSE 流式使用示例

## 🏗️ 项目结构

```
easemob-doc-search/
├── src/                    # TypeScript 源码
│   ├── index.ts           # 主入口文件
│   ├── client.ts          # 客户端类
│   ├── server.ts          # Express 服务器
│   ├── mcp-server.ts      # MCP 服务器
│   ├── services/          # 服务层
│   │   └── doc-search.service.ts
│   ├── types.ts           # 类型定义
│   └── cli.ts             # 命令行工具
├── dist/                  # 编译后的 JavaScript
├── examples/              # 使用示例
├── document/              # 文档目录
├── scripts/               # 脚本文件
├── package.json           # npm 包配置
├── tsconfig.json          # TypeScript 配置
├── Dockerfile             # Docker 配置
└── docker-compose.yml     # Docker Compose 配置
```

## 🐳 Docker 部署

### 使用 Docker Compose

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 使用 Docker 命令

```bash
# 构建镜像
docker build -t easemob-doc-search .

# 运行容器
docker run -d \
  --name easemob-doc-search \
  -p 8000:8000 \
  -v $(pwd)/document:/app/document:ro \
  easemob-doc-search
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