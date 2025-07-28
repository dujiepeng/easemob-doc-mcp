# 部署指南

本文档介绍如何部署环信文档搜索服务。

## 🚀 快速开始

### 1. 使用 Docker（推荐）

#### 使用 Docker Compose

```bash
# 克隆项目
git clone https://github.com/easemob/easemob-doc-search.git
cd easemob-doc-search

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 使用 Docker 命令

```bash
# 构建镜像
docker build -t easemob-doc-search .

# 运行容器
docker run -d \
  --name easemob-doc-search \
  -p 8000:8000 \
  -v $(pwd)/document:/app/document:ro \
  easemob-doc-search

# 查看日志
docker logs -f easemob-doc-search
```

### 2. 本地部署

#### 环境要求

- Python 3.8+
- Node.js 16+（可选，用于npm包）

#### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/easemob/easemob-doc-search.git
cd easemob-doc-search

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 启动服务
cd fastmcp_server
python main.py --mode api
```

### 3. 使用 npm 包

```bash
# 安装包
npm install easemob-doc-search

# 使用命令行工具
npx easemob-doc-search health
npx easemob-doc-search search android
npx easemob-doc-search serve
```

## 🌐 生产环境部署

### 1. 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # SSE 支持
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 86400;
    }
}
```

### 2. 使用 PM2 进程管理

```bash
# 安装 PM2
npm install -g pm2

# 创建 PM2 配置文件
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'easemob-doc-search',
    script: 'fastmcp_server/main.py',
    interpreter: 'python',
    args: '--mode api',
    cwd: '/path/to/easemob-doc-search',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    }
  }]
}
EOF

# 启动服务
pm2 start ecosystem.config.js

# 查看状态
pm2 status

# 查看日志
pm2 logs easemob-doc-search
```

### 3. 使用 Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: easemob-doc-search
spec:
  replicas: 3
  selector:
    matchLabels:
      app: easemob-doc-search
  template:
    metadata:
      labels:
        app: easemob-doc-search
    spec:
      containers:
      - name: easemob-doc-search
        image: easemob/easemob-doc-search:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: easemob-doc-search-service
spec:
  selector:
    app: easemob-doc-search
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

## 🔧 配置选项

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `PORT` | `8000` | 服务端口 |
| `HOST` | `0.0.0.0` | 服务地址 |
| `MODE` | `api` | 运行模式 (api/mcp/both) |
| `LOG_LEVEL` | `INFO` | 日志级别 |

### 使用环境变量

```bash
# Docker
docker run -d \
  -e PORT=9000 \
  -e MODE=both \
  -p 9000:9000 \
  easemob-doc-search

# 本地
PORT=9000 MODE=both python fastmcp_server/main.py
```

## 📊 监控和日志

### 健康检查

```bash
# 检查服务状态
curl http://localhost:8000/health

# 预期响应
{
  "status": "healthy",
  "service": "easemob-doc-search"
}
```

### 日志配置

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 🔒 安全配置

### 1. 启用 HTTPS

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        # ... 其他配置
    }
}
```

### 2. 添加认证

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    if not is_valid_token(token.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token.credentials

@app.get("/api/search-docs")
async def api_search_docs(
    platform: str = Query(...),
    token: str = Depends(verify_token)
):
    # ... 实现
```

## 🚀 性能优化

### 1. 启用缓存

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/api/search-docs")
@cache(expire=300)  # 缓存5分钟
async def api_search_docs(platform: str):
    # ... 实现
```

### 2. 负载均衡

```nginx
upstream easemob_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    location / {
        proxy_pass http://easemob_backend;
        # ... 其他配置
    }
}
```

## 📝 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查看端口占用
   lsof -i :8000
   
   # 杀死进程
   kill -9 <PID>
   ```

2. **权限问题**
   ```bash
   # 修改文件权限
   chmod +x fastmcp_server/main.py
   ```

3. **依赖问题**
   ```bash
   # 重新安装依赖
   pip install -r requirements.txt --force-reinstall
   ```

### 日志分析

```bash
# 查看错误日志
grep ERROR app.log

# 查看访问日志
tail -f access.log
```

## 📞 支持

如果遇到问题，请：

1. 查看 [GitHub Issues](https://github.com/easemob/easemob-doc-search/issues)
2. 提交新的 Issue
3. 联系技术支持团队 