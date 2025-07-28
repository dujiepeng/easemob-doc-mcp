# 环信文档搜索服务

一个基于Node.js的环信文档搜索服务，支持多平台文档搜索、SSE流式响应和Model Context Protocol (MCP)。

## ✨ 特性

- 🔍 **多平台文档搜索**: 支持Android、iOS、Web、Flutter、React Native等平台
- 📡 **SSE流式响应**: 实时流式返回搜索结果
- 🤖 **MCP协议支持**: 与Cursor等AI编辑器无缝集成
- 📦 **npm包支持**: 可直接通过npx使用
- 🐳 **Docker部署**: 支持容器化部署
- 🔧 **RESTful API**: 提供完整的HTTP API接口

## 🚀 快速开始

### 作为npm包使用

#### 安装和使用

```bash
# 直接使用npx
npx @easemob/docs-mcp@latest

# 或者全局安装
npm install -g @easemob/docs-mcp
easemob-doc-search --help
```

#### 基本使用

```javascript
const EasemobDocSearchClient = require('@easemob/docs-mcp');

// 创建客户端
const client = new EasemobDocSearchClient({
  baseUrl: 'http://localhost:8000'
});

// 搜索文档
const result = await client.searchDocs('android');
console.log(`找到 ${result.results.length} 个文档`);

// 获取文档内容
const content = await client.getDocContent('android/quickstart.md');
console.log(content.content);
```

#### SSE流式使用

```javascript
const EasemobDocSearchClient = require('@easemob/docs-mcp');

const client = new EasemobDocSearchClient({
  baseUrl: 'http://localhost:8000'
});

// 流式搜索
for await (const event of client.searchDocsStream('android')) {
  switch (event.type) {
    case 'start':
      console.log('开始搜索...');
      break;
    case 'progress':
      console.log(`进度: ${event.message}`);
      break;
    case 'results_batch':
      console.log(`找到 ${event.data?.length || 0} 个文档`);
      break;
    case 'complete':
      console.log('搜索完成');
      break;
  }
}
```

### 命令行工具

```bash
# 搜索文档
npx @easemob/docs-mcp@latest search android

# 获取文档内容
npx @easemob/docs-mcp@latest content android/quickstart.md

# 健康检查
npx @easemob/docs-mcp@latest health

# 流式搜索
npx @easemob/docs-mcp@latest stream-search android

# 启动服务器
npx @easemob/docs-mcp@latest serve --port 8000 --mode both
```

## 🎯 在Cursor中使用

### 自动配置

```bash
# 运行配置脚本
npx @easemob/docs-mcp@latest setup-cursor
```

### 手动配置

在Cursor的MCP配置文件中添加：

```json
{
  "easemob-docs": {
    "command": "npx",
    "args": ["@easemob/docs-mcp@latest"]
  }
}
```

### 使用示例

在Cursor中，你可以直接使用以下MCP工具：

- `search_platform_docs`: 搜索平台文档
- `get_document_content`: 获取文档内容
- `get_available_platforms`: 获取可用平台列表
- `get_document_stats`: 获取文档统计信息

## 🛠️ 本地开发

### 环境要求

- Node.js 16+
- npm 或 yarn

### 安装依赖

```bash
npm install
```

### 构建项目

```bash
npm run build
```

### 启动开发服务器

```bash
# 启动API服务器
npm run start:dev

# 启动MCP服务器
npm run mcp:dev

# 启动客户端
npm run mcp-client:dev
```

### 测试

```bash
# 运行所有测试
npm test

# 测试基本功能
npm run test:basic

# 测试SSE功能
npm run test:sse
```

## 📡 API接口

### REST API

- `GET /health` - 健康检查
- `GET /api/search-docs?platform=<platform>` - 搜索文档
- `GET /api/get-doc-content?path=<path>&keyword=<keyword>` - 获取文档内容

### SSE接口

- `GET /api/sse/search-docs?platform=<platform>` - 流式搜索文档
- `GET /api/sse/get-doc-content?path=<path>&keyword=<keyword>` - 流式获取文档内容

## 🐳 Docker部署

### 构建镜像

```bash
docker build -t easemob-doc-search .
```

### 运行容器

```bash
docker run -p 8000:8000 easemob-doc-search
```

### Docker Compose

```bash
docker-compose up -d
```

## 📦 发布npm包

### 构建和发布

```bash
# 构建项目
npm run build

# 发布到npm
npm publish
```

### 版本管理

```bash
# 更新版本号
npm version patch  # 补丁版本
npm version minor  # 次要版本
npm version major  # 主要版本
```

## 📁 项目结构

```
easemob-doc-mcp2/
├── src/
│   ├── server.ts              # Express服务器
│   ├── mcp-server.ts          # MCP服务器
│   ├── mcp-client.ts          # MCP客户端
│   ├── client.ts              # HTTP客户端
│   ├── cli.ts                 # 命令行工具
│   ├── index.ts               # 包入口
│   ├── types.ts               # 类型定义
│   └── services/
│       └── doc-search.service.ts  # 文档搜索服务
├── document/                  # 文档目录
├── dist/                      # 编译输出
├── scripts/                   # 脚本文件
├── test/                      # 测试文件
├── examples/                  # 使用示例
├── package.json
├── tsconfig.json
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🔧 配置选项

### 环境变量

- `PORT`: 服务器端口 (默认: 8000)
- `NODE_ENV`: 运行环境 (development/production)
- `EASEMOB_API_URL`: API服务器地址 (用于MCP客户端)

### 客户端选项

```typescript
interface ClientOptions {
  baseUrl?: string;        // API基础URL
  timeout?: number;        // 请求超时时间
  headers?: Record<string, string>;  // 自定义请求头
}
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [环信官网](https://www.easemob.com/)
- [环信文档](https://docs.easemob.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Cursor编辑器](https://cursor.sh/) 