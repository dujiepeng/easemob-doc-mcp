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

### 安装

```bash
npm install
npm run build
```

### 启动服务

```bash
# 启动API服务器
npm start

# 启动MCP服务器
npm run mcp

# 开发模式
npm run start:dev
```

### 使用CLI

```bash
# 搜索文档
npm run cli search android

# 获取文档内容
npm run cli content android/quickstart.md

# 查看帮助
npm run cli --help
```

### 作为npm包使用

```bash
# 直接使用npx
npx @easemob/docs-mcp@latest search android

# 全局安装
npm install -g @easemob/docs-mcp
@easemob/docs-mcp search android
```

## 📡 API接口

### REST API

- `GET /health` - 健康检查
- `GET /api/search-docs?platform={platform}` - 搜索文档
- `GET /api/get-doc-content?path={path}&keyword={keyword}` - 获取文档内容

### SSE流式API

- `GET /api/sse/search-docs?platform={platform}` - 流式搜索
- `GET /api/sse/get-doc-content?path={path}&keyword={keyword}` - 流式获取内容

## 🤖 Cursor集成

### 快速配置

```bash
npm run setup-cursor
```

### 手动配置

在Cursor的MCP设置中添加：

```json
{
  "easemob-docs": {
    "command": "npx",
    "args": ["@easemob/docs-mcp@latest"],
    "description": "环信文档搜索服务"
  }
}
```

## 📦 项目结构

```
src/
├── server.ts          # Express API服务器
├── mcp-server.ts      # MCP服务器
├── client.ts          # HTTP客户端
├── cli.ts             # 命令行工具
├── types.ts           # 类型定义
├── index.ts           # 主入口
└── services/
    └── doc-search.service.ts  # 文档搜索服务
```

## 🛠️ 开发

```bash
# 安装依赖
npm install

# 开发模式
npm run start:dev

# 构建
npm run build

# 测试
npm run mcp
```

## �� 许可证

MIT License 