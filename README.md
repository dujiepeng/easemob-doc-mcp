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
- 支持多种传输模式（HTTP、stdio、SSE）
- 支持定期自动更新文档

## 安装

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 确保 `document` 和 `uikit` 目录存在于项目根目录中

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

#### 方式一：HTTP 传输模式（适用于服务器部署）

1. 确保 MCP 服务器正在运行：
   ```bash
   python src/server.py --port 9000
   ```

2. 在 Cursor 的 MCP 配置中添加：

```json
{
  "easemob-doc-mcp": {
    "transport": "http",
    "url": "http://127.0.0.1:9000/mcp/",
    "description": "环信文档搜索工具"
  }
}
```

#### 方式二：stdio 传输模式（推荐用于本地调试）

stdio 传输模式是最适合本地开发和调试的方式，它不需要开放网络端口，更加安全和便捷。

1. 在 Cursor 的 MCP 配置中添加：

```json
{
  "easemob-doc-mcp": {
    "transport": "stdio",
    "command": "python /完整路径/easemob-doc-mcp/src/server.py --transport stdio",
    "description": "环信文档搜索工具"
  }
}
```

注意：
- 必须使用绝对路径，例如：`/Users/username/AI/mcp-server/easemob-doc-mcp/src/server.py`
- 使用 stdio 模式时，不需要手动启动服务，Cursor 会在需要时自动启动
- 如果遇到 Python 环境问题，可以指定完整的 Python 路径：
  ```json
  "command": "/path/to/python /path/to/easemob-doc-mcp/src/server.py --transport stdio"
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
   
   默认配置使用端口9000，您可以在docker-compose.yml文件中修改端口映射：
   ```yaml
   ports:
     - "9000:9000"  # 主机端口:容器端口
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
- `doc_type` (string): 文档类型，必填参数，只能为 'sdk' 或 'uikit'
  - 'sdk': 搜索 document 目录下的文档
  - 'uikit': 搜索 uikit 目录下的文档
- `platform` (string): 平台名称，如 'android', 'ios', 'web', 'flutter', 'react-native', 'applet', 'server-side' 等
  - 支持部分匹配，例如输入 'and' 会匹配 'android'
  - 支持常用词语映射：'小程序' -> 'applet', '鸿蒙' -> 'harmonyos', 'rn' -> 'react-native', 'rest' -> 'server-side'

**返回：**
- 匹配的文档路径列表，根据 doc_type 参数返回 document 或 uikit 目录下的相关文档

**示例：**
```python
# 搜索Android平台SDK文档
docs = await mcp.call("search_platform_docs", {"doc_type": "sdk", "platform": "android"})

# 搜索UIKit文档
uikit_docs = await mcp.call("search_platform_docs", {"doc_type": "uikit", "platform": "chat"})
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
│   ├── ios/               # iOS文档
│   ├── web/               # Web文档
│   └── ...                # 其他平台文档
├── uikit/                 # UIKit文档目录
│   ├── chatuikit/         # 聊天UIKit文档
│   ├── chatroomuikit/     # 聊天室UIKit文档
│   └── README.md          # UIKit说明文档
├── tests/                 # 测试目录
│   └── test_mcp_official.py # 测试脚本
├── pyproject.toml         # 项目配置
├── requirements.txt       # 依赖列表
├── install.sh             # 一键安装脚本
├── uninstall.sh           # 卸载脚本
├── deploy.sh              # 部署脚本
├── update_docs.sh         # 文档更新脚本
├── setup_cron.sh          # 定时更新配置脚本
├── Dockerfile             # Docker配置
├── docker-compose.yml     # Docker Compose配置
└── easemob-doc-mcp.conf   # Supervisor配置
```

## 开发

### 安装开发依赖

```bash
# 安装项目及其依赖（开发模式）
pip install -e .

# 或直接安装依赖
pip install -r requirements.txt
```

### 自动更新文档

设置定时任务，每天自动从GitHub拉取最新文档：

```bash
# 赋予脚本执行权限
chmod +x setup_cron.sh

# 设置定时任务（默认每天凌晨3点执行）
./setup_cron.sh
```

### 运行测试

测试服务是否正常工作：

```bash
# 启动服务
python src/server.py --port 9000

# 在另一个终端中运行测试脚本
python tests/test_mcp_official.py
```

服务器启动后，可以通过 MCP 客户端进行测试。

## 本地调试最佳实践

### 使用 stdio 模式进行本地开发

使用 stdio 传输模式是本地开发和调试的最佳选择，具有以下优势：

1. **安全性**：不需要开放网络端口，降低安全风险
2. **便捷性**：无需手动启动服务，Cursor 会在需要时自动启动和管理
3. **稳定性**：避免端口冲突和网络相关问题
4. **资源效率**：服务仅在需要时运行，不会持续占用系统资源

### 调试步骤

1. **配置环境**：
   ```bash
   # 创建并激活虚拟环境（推荐）
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # 或
   venv\Scripts\activate  # Windows
   
   # 安装依赖
   pip install -r requirements.txt
   
   # 拉取最新文档（可选）
   chmod +x update_docs.sh
   ./update_docs.sh
   ```

2. **配置 Cursor**：
   - 打开 Cursor 设置
   - 找到 MCP 配置部分
   - 添加配置（使用您的实际路径）：
   ```json
   {
     "easemob-doc-mcp": {
       "transport": "stdio",
       "command": "python /Users/你的用户名/AI/mcp-server/easemob-doc-mcp/src/server.py --transport stdio"
     }
   }
   ```

3. **测试服务**：
   - 在 Cursor 中使用 `@easemob-doc-mcp` 调用服务
   - 示例：`@easemob-doc-mcp search_platform_docs {"platform": "android"}`

4. **调试技巧**：
   - 如果遇到问题，检查 Cursor 的日志输出
   - 可以临时修改 `server.py` 添加调试打印语句
   - 使用 Python 的 logging 模块记录详细日志

### 常见问题解决

1. **找不到模块**：
   - 确保已安装所有依赖 `pip install -r requirements.txt`
   - 检查 Python 环境路径是否正确

2. **权限问题**：
   - 确保脚本有执行权限 `chmod +x src/server.py`
   - 检查文档目录的读取权限

3. **路径问题**：
   - 使用绝对路径避免相对路径引起的问题
   - 确保路径中没有特殊字符或空格 