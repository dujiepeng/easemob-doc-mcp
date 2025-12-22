# 环信文档搜索 MCP 服务 (Easemob Doc MCP)

这是一个基于 [FastMCP](https://github.com/jlowin/fastmcp) 构建的 MCP (Model Context Protocol) 服务，旨在帮助 LLM (如 Claude, Cursor) 快速检索和理解环信 (Easemob) 的技术文档。

它集成了 **Whoosh 全文搜索引擎** 和 **jieba 中文分词**，支持自然语言问答和精确的文档定位。

## ✨ 主要功能

*   **🔍 全文智能搜索** (`search_knowledge_base`):
    *   支持自然语言提问（如 "Android 登录失败怎么排查？"）。
    *   基于 BM25 算法的相关性排序。
    *   精准的中文分词与高亮摘要返回。
*   **📂 目录结构浏览** (`search_platform_docs`):
    *   浏览 SDK, UIKit, CallKit 的特定平台文档结构。
*   **🔄 docker 自动更新 & 按需同步**:
    *   Docker 容器构建时不再依赖本地文档文件夹。
    *   启动时会自动执行 `git clone` 拉取文档仓库、UIKit 仓库和 CallKit 仓库。
    *   内置定时任务，每天自动执行 `git pull` 同步最新文档并重建索引。

## 🛠️ Docker 部署 (推荐)

最简单的部署方式是使用 Docker。我们提供了开箱即用的配置。

### 1. 启动服务

在项目根目录下运行：

```bash
docker-compose up --build -d
```

*   服务将在 `9000` 端口启动 (SSE 模式)。
*   首次启动会自动从远程仓库拉取文档，并构建全文索引（根据网络情况可能需要一点时间）。

### 2. 外网访问 (可选)

配置中已集成 **Cloudflare Tunnel**，启动后会自动建立安全隧道，以便您在公网环境下也能访问此 MCP 服务。

1. 在项目根目录创建 `.env` 文件：
   ```bash
   CLOUDFLARE_TUNNEL_TOKEN=您的隧道Token
   ```
2. 运行以下命令启动包含隧道的全量服务：
```bash
docker-compose up -d
```

### 2. 自动更新机制

默认情况下，容器会 **每 24 小时** 执行一次 `git pull`：
*   如果检测到文档更新：自动重建索引 + 清理缓存。
*   如果无更新：静默待机。

您可以通过环境变量调整更新频率（单位：秒）：

```bash
# 例如：每 1 小时更新一次
export DOC_UPDATE_INTERVAL_SECONDS=3600
docker-compose up -d
```

### 3. Docker 模式下的本地链接

在 `docker-compose.yml` 中，我们将当前目录挂载到了容器的 `/app` 目录：

```yaml
volumes:
  - .:/app
```

这意味着：
*   **双向同步**：容器内对文档的更新（`git pull`）和索引的构建会直接反映在宿主机的磁盘上。
*   **开发便利**：您可以在宿主机上直接修改 `src/` 下的代码，容器会自动应用这些更改（如果使用了支持热重载的机制，或者重启容器 `docker-compose restart`）。
*   **环境一致**：即便在不同机器上，只要运行 Docker，就能获得完全一致的搜索环境和依赖配置。

## 🔌 MCP Client 使用指南

部署成功后，您可以将此服务连接到支持 MCP 的客户端。

### Cursor 使用

1.  打开 Cursor 设置 -> **Features** -> **MCP Servers**。
2.  点击 **+ Add new MCP server**。
3.  填写配置：
    *   **Name**: `Easemob Docs`
    *   **Type**: `command` (本地运行) 或 `sse` (Docker 远程)
    
    **方式 A: Docker (SSE)**
    *   **Url**: `http://localhost:9000/sse`

    **方式 B: 本地运行 (SSE)**
    *   首先在项目根目录启动服务：
        ```bash
        python src/server.py --port 9000 --transport sse --path /sse
        ```
    *   在 Cursor 中填写：
        *   **Url**: `http://localhost:9000/sse`

    **方式 C: 本地运行 (Command - 传统模式)**
    *   **Command**: `python /绝对路径/to/easemob-doc-mcp/src/server.py`
    *   (注意：推荐使用 SSE 模式，因为它在处理长连接和多查询时更稳定)

### Claude Desktop 使用

修改您的 Claude 配置文件 (`~/Library/Application Support/Claude/claude_desktop_config.json`)：

```json
{
  "mcpServers": {
    "easemob-docs": {
      "url": "https://mcp-servers.dujiepeng.top/sse"
    }
  }
}
```

## 🧪 调试与验证

我们提供了一个调试脚本，可以直观地查看搜索效果：

```bash
python debug_search.py
```

它会模拟几次搜索请求，并展示高亮结果。

> [!NOTE]
> 启动日志中应显示：`启动环信文档搜索MCP服务器 (v1.1.8 - Full Text Search)`

## 📦 这个项目包含什么？

*   `src/server.py`: MCP 服务器核心逻辑（包含文档同步逻辑）。
*   `src/indexer.py`: Whoosh 搜索引擎封装。
*   `document/`, `uikit/`, `callkit/`: 自动同步生成的环信技术文档（容器运行时拉取，无需手动准备）。
*   `indexdir/`: 自动生成的索引文件（请勿提交到 Git）。

## ⚙️ 环境变量

| 变量 | 描述 | 默认值 |
| --- | --- | --- |
| `DOC_REPO_URL` | 文档仓库 Git 地址 | `https://github.com/easemob/easemob-doc.git` |
| `UIKIT_REPO_URL` | UIKit 仓库 Git 地址 | `https://github.com/easemob/easemob-uikit-doc.git` |
| `CALLKIT_REPO_URL` | CallKit 仓库 Git 地址 | `https://github.com/easemob/easemob-callkit-doc.git` |
| `DOC_UPDATE_INTERVAL_SECONDS` | 文档更新时间间隔 (秒) | `86400` (24小时) |
| `CLOUDFLARE_TUNNEL_TOKEN` | Cloudflare Tunnel 令牌 | (无) |


## License

MIT