# Cursor 集成指南 - Docker 部署版本

## 🐳 Docker 部署

### 1. 构建和运行 Docker 容器

```bash
# 构建镜像
docker build -t easemob-doc-search .

# 运行容器
docker run -d \
  --name easemob-doc-search \
  -p 8000:8000 \
  -v $(pwd)/document:/app/document:ro \
  easemob-doc-search

# 或者使用 Docker Compose
docker-compose up -d
```

### 2. 验证部署

```bash
# 检查容器状态
docker ps

# 测试 API
curl http://localhost:8000/health

# 测试搜索功能
curl "http://localhost:8000/api/search-docs?platform=android"
```

## 🤖 Cursor 配置方式

### 方式一：直接使用远程 URL（推荐）

在 Cursor 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "easemob-docs": {
      "command": "npx",
      "args": ["@easemob/docs-mcp@latest", "mcp-remote"],
      "env": {
        "EASEMOB_API_URL": "http://your-server.com:8000"
      },
      "description": "环信文档搜索服务 - 远程部署"
    }
  }
}
```

### 方式二：使用本地 MCP 客户端

```json
{
  "mcpServers": {
    "easemob-docs": {
      "command": "node",
      "args": ["/path/to/your/project/dist/mcp-client.js"],
      "env": {
        "EASEMOB_API_URL": "http://your-server.com:8000"
      },
      "description": "环信文档搜索服务 - 本地客户端"
    }
  }
}
```

### 方式三：使用 npx 远程客户端

```json
{
  "mcpServers": {
    "easemob-docs": {
      "command": "npx",
      "args": ["@easemob/docs-mcp@latest", "mcp-remote"],
      "env": {
        "EASEMOB_API_URL": "https://your-production-server.com"
      },
      "description": "环信文档搜索服务"
    }
  }
}
```

## 🌐 不同部署场景

### 本地 Docker 部署

```json
{
  "mcpServers": {
    "easemob-docs": {
      "command": "npx",
      "args": ["@easemob/docs-mcp@latest", "mcp-remote"],
      "env": {
        "EASEMOB_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

### 云服务器部署

```json
{
  "mcpServers": {
    "easemob-docs": {
      "command": "npx",
      "args": ["@easemob/docs-mcp@latest", "mcp-remote"],
      "env": {
        "EASEMOB_API_URL": "https://your-server.com"
      }
    }
  }
}
```

### 内网部署

```json
{
  "mcpServers": {
    "easemob-docs": {
      "command": "npx",
      "args": ["@easemob/docs-mcp@latest", "mcp-remote"],
      "env": {
        "EASEMOB_API_URL": "http://192.168.1.100:8000"
      }
    }
  }
}
```

## 🔧 环境变量配置

### 支持的环境变量

- `EASEMOB_API_URL`: 远程服务器地址（必需）
- `NODE_ENV`: 运行环境（可选，默认 production）

### 配置示例

```bash
# 设置环境变量
export EASEMOB_API_URL="https://your-server.com"

# 运行远程客户端
npm run mcp-remote
```

## 📋 可用的 MCP 工具

配置完成后，你可以在 Cursor 中使用以下工具：

1. **search_platform_docs**: 搜索平台文档
   - 参数: `platform` (string) - 平台名称

2. **get_document_content**: 获取文档内容
   - 参数: `doc_path` (string) - 文档路径
   - 参数: `keyword` (string, 可选) - 搜索关键词

3. **get_available_platforms**: 获取可用平台列表

4. **get_document_stats**: 获取文档统计信息

## 🚀 部署到生产环境

### 1. 云服务器部署

```bash
# 在服务器上
git clone <your-repo>
cd easemob-doc-mcp2
docker-compose up -d

# 配置防火墙
sudo ufw allow 8000
```

### 2. 使用反向代理（推荐）

```nginx
# Nginx 配置
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. 使用 HTTPS

```bash
# 使用 Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

## 🔍 故障排除

### 1. 连接失败

```bash
# 检查服务器是否运行
curl http://your-server.com:8000/health

# 检查网络连接
ping your-server.com

# 检查防火墙
sudo ufw status
```

### 2. MCP 客户端错误

```bash
# 检查环境变量
echo $EASEMOB_API_URL

# 手动测试连接
npm run mcp-remote:dev
```

### 3. Docker 容器问题

```bash
# 查看容器日志
docker logs easemob-doc-search

# 重启容器
docker restart easemob-doc-search

# 检查容器状态
docker ps -a
```

## 📝 使用示例

在 Cursor 中，你可以这样使用：

```
请帮我搜索 Android 平台的文档
```

MCP 会自动调用 `search_platform_docs` 工具，连接到你的 Docker 部署的服务。

```
请获取 android/quickstart.md 的内容
```

MCP 会调用 `get_document_content` 工具获取文档内容。 