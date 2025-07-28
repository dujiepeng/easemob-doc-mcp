# 迁移指南：从 Python 到 Node.js

本文档说明如何从 Python 版本的环信文档搜索服务迁移到纯 Node.js 实现。

## 🚀 主要变化

### 1. 技术栈变更

| 组件 | 旧版本 (Python) | 新版本 (Node.js) |
|------|----------------|------------------|
| 服务器框架 | FastAPI | Express.js |
| MCP 实现 | FastMCP | @modelcontextprotocol/sdk |
| 包管理 | pip + requirements.txt | npm + package.json |
| 运行时 | Python 3.8+ | Node.js 16+ |

### 2. 文件结构变化

```
旧结构 (Python):
├── fastmcp_server/
│   ├── main.py
│   ├── run_mcp.py
│   └── client_example.py
├── requirements.txt
└── ...

新结构 (Node.js):
├── src/
│   ├── server.ts          # Express 服务器
│   ├── mcp-server.ts      # MCP 服务器
│   ├── client.ts          # 客户端类
│   ├── services/
│   │   └── doc-search.service.ts
│   ├── types.ts
│   ├── cli.ts
│   └── index.ts
├── dist/                  # 编译后的 JS
├── package.json
└── ...
```

## 📦 安装和部署

### 旧版本 (Python)

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务器
cd fastmcp_server
python main.py --mode api
```

### 新版本 (Node.js)

```bash
# 安装依赖
npm install

# 构建项目
npm run build

# 启动服务器
npm start
```

## 🔧 配置变更

### Cursor MCP 配置

#### 旧版本
```json
{
  "docs-search": {
    "command": "python",
    "args": ["/path/to/fastmcp_server/run_mcp.py"],
    "env": {},
    "description": "环信文档搜索服务"
  }
}
```

#### 新版本
```json
{
  "docs-search": {
    "command": "node",
    "args": ["/path/to/dist/mcp-server.js"],
    "env": {},
    "description": "环信文档搜索服务"
  }
}
```

## 🐳 Docker 部署

### 旧版本 Dockerfile
```dockerfile
FROM python:3.11-slim
# ... Python 相关配置
CMD ["python", "fastmcp_server/main.py", "--mode", "api"]
```

### 新版本 Dockerfile
```dockerfile
FROM node:18-alpine
# ... Node.js 相关配置
CMD ["node", "dist/server.js"]
```

## 📡 API 兼容性

### REST API 端点

所有 REST API 端点保持完全兼容：

- `GET /health` - 健康检查
- `GET /api/search-docs?platform={platform}` - 搜索文档
- `GET /api/get-doc-content?path={path}&keyword={keyword}` - 获取文档内容

### SSE 端点

SSE 端点也保持完全兼容：

- `GET /api/sse/search-docs?platform={platform}` - 流式搜索
- `GET /api/sse/get-doc-content?path={path}&keyword={keyword}` - 流式获取内容

## 🔄 迁移步骤

### 1. 备份现有数据
```bash
# 备份文档目录
cp -r document document_backup
```

### 2. 更新代码
```bash
# 拉取新版本
git pull origin main

# 删除旧文件
rm -rf fastmcp_server
rm requirements.txt
```

### 3. 安装新依赖
```bash
# 安装 Node.js 依赖
npm install

# 构建项目
npm run build
```

### 4. 更新配置
- 更新 Cursor MCP 配置
- 更新 Docker 配置（如果使用）
- 更新部署脚本

### 5. 测试功能
```bash
# 启动服务器
npm start

# 测试基本功能
npm run test:basic

# 测试 SSE 功能
npm run test:sse
```

## 🆕 新功能

### 1. 更好的开发体验
- TypeScript 支持
- 热重载开发模式
- 更好的错误处理

### 2. 增强的 CLI 工具
```bash
# 新增统计命令
easemob-doc-search stats

# 更好的错误提示
easemob-doc-search health
```

### 3. 改进的 MCP 支持
- 更稳定的 MCP 服务器
- 更好的错误处理
- 支持更多工具

## 🐛 常见问题

### Q: 为什么迁移到 Node.js？
A: 
- 更好的包管理和发布体验
- 统一的 JavaScript/TypeScript 生态
- 更好的性能和可维护性
- 更容易部署和扩展

### Q: 现有客户端代码需要修改吗？
A: 不需要。所有 API 端点保持完全兼容，现有客户端代码可以继续使用。

### Q: 如何回滚到 Python 版本？
A: 可以切换到旧的分支或标签：
```bash
git checkout python-version
```

### Q: 性能有影响吗？
A: Node.js 版本在大多数场景下性能更好，特别是在并发处理方面。

## 📞 支持

如果在迁移过程中遇到问题：

1. 查看 [GitHub Issues](https://github.com/easemob/easemob-doc-search/issues)
2. 提交新的 Issue
3. 联系技术支持团队

## 🎉 迁移完成检查清单

- [ ] 安装 Node.js 16+
- [ ] 安装项目依赖 (`npm install`)
- [ ] 构建项目 (`npm run build`)
- [ ] 测试基本功能 (`npm run test:basic`)
- [ ] 测试 SSE 功能 (`npm run test:sse`)
- [ ] 更新 Cursor MCP 配置
- [ ] 更新部署配置（Docker、PM2 等）
- [ ] 验证生产环境部署 