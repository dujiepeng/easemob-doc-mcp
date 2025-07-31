# 环信文档搜索 MCP 服务

这是一个基于 FastMCP 构建的环信文档搜索服务，用于搜索和检索环信各平台的技术文档。

## 🚀 一键部署

### 快速安装（推荐）

```bash
# 使用默认配置 (HTTP传输，端口443)
bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/install.sh)

# 指定自定义端口
bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/install.sh) --port 8080

# 指定传输协议和完整参数
bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/install.sh) --transport http --port 443 --host 0.0.0.0 --path /mcp/

# 使用stdio传输（无需端口配置）
bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/install.sh) --transport stdio

# 使用SSE传输
bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/install.sh) --transport sse --port 8080

# 查看帮助信息
bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/install.sh) --help
```

### 卸载

```bash
# 卸载默认配置服务
bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/uninstall.sh)

# 卸载指定端口服务
bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/uninstall.sh) --port 8080

# 卸载指定传输协议服务
bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/uninstall.sh) --transport http --port 443 --host 0.0.0.0 --path /mcp/
```

## 功能特点

- 按平台搜索文档（Android、iOS、Web、Flutter、React Native等）
- 获取文档全文内容
- 在文档中搜索关键字并返回上下文
- 支持 MCP 协议，可与 Cursor 等工具集成
- 支持自定义端口部署

## 安装

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 确保 `document` 目录存在于项目根目录中

## 使用方法

### 本地开发

```bash
# 使用默认配置 (HTTP传输，端口443)
python src/server.py

# 指定端口
python src/server.py --port 8080

# 指定传输协议和完整参数
python src/server.py --transport http --port 443 --host 0.0.0.0 --path /mcp/

# 使用stdio传输（适用于本地开发）
python src/server.py --transport stdio

# 使用SSE传输
python src/server.py --transport sse --port 8080

# 查看帮助信息
python src/server.py --help
```

服务器将在指定的配置上运行，提供 MCP 服务。

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

## 服务器部署

### 方案1：使用 systemd 服务（推荐）

1. 运行部署脚本：
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

2. 管理服务：
   ```bash
   # 查看服务状态
   sudo systemctl status easemob-doc-mcp
   
   # 启动服务
   sudo systemctl start easemob-doc-mcp
   
   # 停止服务
   sudo systemctl stop easemob-doc-mcp
   
   # 重启服务
   sudo systemctl restart easemob-doc-mcp
   
   # 查看日志
   sudo journalctl -u easemob-doc-mcp -f
   ```

### 方案2：使用 Docker 部署

1. 构建并启动容器：
   ```bash
   docker-compose up -d
   ```

2. 管理容器：
   ```bash
   # 查看容器状态
   docker-compose ps
   
   # 查看日志
   docker-compose logs -f
   
   # 重启服务
   docker-compose restart
   
   # 停止服务
   docker-compose down
   ```

### 方案3：使用 Supervisor 管理

1. 安装 Supervisor：
   ```bash
   sudo apt-get install supervisor
   ```

2. 复制配置文件：
   ```bash
   sudo cp easemob-doc-mcp.conf /etc/supervisor/conf.d/
   sudo supervisorctl reread
   sudo supervisorctl update
   ```

3. 管理服务：
   ```bash
   # 启动服务
   sudo supervisorctl start easemob-doc-mcp
   
   # 停止服务
   sudo supervisorctl stop easemob-doc-mcp
   
   # 重启服务
   sudo supervisorctl restart easemob-doc-mcp
   
   # 查看状态
   sudo supervisorctl status
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
├── requirements.txt      # 依赖列表
├── install.sh           # 一键安装脚本
├── uninstall.sh         # 卸载脚本
├── deploy.sh            # 部署脚本
├── Dockerfile           # Docker配置
├── docker-compose.yml   # Docker Compose配置
└── easemob-doc-mcp.conf # Supervisor配置
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