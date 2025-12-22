# Changelog

## [1.1.12] - 2025-12-22

### 性能优化 (Performance Optimizations)
- **同步加速**: 将文档同步方式从 `git clone` 优化为直接下载 Zip 归档。
- **效率提升**: 移除了 Git 历史记录的下载，大幅减少了同步时间和带宽占用。
- **依赖精简**: 使用 Python 内置的 `zipfile` 和 `urllib` 进行处理，保持环境简洁。


## [1.1.11] - 2025-12-22

### 修复 (Bug Fixes)
- **代码修复**: 修复了 `ensure_docs_ready` 函数中变量未定义的错误。
- **功能恢复**: 重新启用了 `search_knowledge_base` 工具，确保搜索功能正常。

## [1.1.10] - 2025-12-22

### 功能优化 (Feature Optimizations)
- **启动检查增强**: 在服务启动时增加显式的文档目录完整性检查。如果发现 `document/`, `uikit/`, `callkit/` 缺失或为空，将立即触发紧急同步拉取。
- **鲁棒性提升**: 即使文档存在但索引缺失，也会在启动时自动重建索引，确保搜索功能可用。

## [1.1.9] - 2025-12-22

### 功能优化 (Feature Optimizations)
- **同步逻辑精细化**: 根据实际仓库结构更新了同步逻辑。现在支持从 `easemob-doc` 仓库的 `doc-v2` 分支提取 `docs/` 下的子目录。
- **配置项变更**: 移除了 `UIKIT_REPO_URL` 和 `CALLKIT_REPO_URL`，新增 `DOC_REPO_BRANCH` 配置。

## [1.1.8] - 2025-12-22

### 功能优化 (Feature Optimizations)
- **运行时文档同步**: 移除了 Docker 构建时对文档文件夹的依赖。现在文档、UIKit 和 CallKit 仓库会在容器启动时自动拉取 (`git clone`)，并定期进行同步 (`git pull`)。
- **环境隔离**: 即使本地没有文档文件夹，也可以成功构建 Docker 镜像。

## [1.1.7] - 2025-12-22

### 修复 (Bug Fixes)
- **SSE 连接修复**: 针对 SSE 初始化报错 `missing endpoint`，重新将服务路径显式设置为 `/sse`，以提高与各 MCP 客户端（特别是通过外网隧道时）的兼容性。

## [1.1.6] - 2025-12-22

### 功能优化 (Feature Optimizations)
- **路径简化**: 将 SSE 服务的默认访问路径从 `/mcp/` 简化为 `/`，使得在使用自定义域名（如 `https://mcp-servers.dujiepeng.top/`）时配置更加直观。
- **文档更新**: README 中的配置示例已更新为最新的根路径格式。

## [1.1.5] - 2025-12-22

### 安全性增强 (Security Enhancements)
- **敏感信息脱敏**: 将 `docker-compose.yml` 中的 Cloudflare Tunnel Token 移至环境变量。现在需要通过根目录下的 `.env` 文件配置 `CLOUDFLARE_TUNNEL_TOKEN`。

## [1.1.4] - 2025-12-22

### 部署增强 (Deployment Enhancements)
- **Cloudflare Tunnel 集成**: 在 `docker-compose.yml` 中增加了 `cloudflared` 服务，支持通过 Cloudflare 隧道实现安全的公网访问。

## [1.1.3] - 2025-12-22

### 文档与功能优化 (Documentation & Feature Optimizations)
- **本地 SSE 指南**: 在 README 中增加了如何以 SSE 模式启动本地服务器的说明，方便用户在不使用 Docker 的情况下也能通过 SSE 协议连接客户端（如 Cursor）。
- **版本一致性**: 修正了启动日志中显示的版本号。

## [1.1.2] - 2025-12-22

### 文档更新 (Documentation Updates)
- **README 增强**: 增加了 Docker 模式下链接本地环境的详细说明，解释了卷挂载的作用及其带来的开发便利性。
- **版本迭代**: 升级至 1.1.2。

## [1.1.1] - 2025-12-19

### 维护与优化 (Maintenance & Optimization)
- **调试信息清理**: 删除了 `get_document_content` 工具中临时添加的 `_debug_info` 字段及 `stderr` 调试打印，保持响应简洁。
- **路径解析增强**: 保留并巩固了对 `sdk/` 前缀路径的自动映射逻辑，确保无论是全文搜索结果还是直接输入路径均能正确访问文件。
- **稳定性提升**: 针对 Docker 环境下的网络问题切换了基础镜像为 `python:3.11-slim-bookworm`，并配置了阿里云和清华大学镜像源，显著提升了构建可靠性和速度。


## [1.1.0] - 2025-12-19

### 新增功能 (New Features)
- **全文搜索引擎**: 引入 `Whoosh` 搜索引擎和 `jieba` 中文分词。
- **智能搜索工具**: 新增 `search_knowledge_base` MCP 工具，支持自然语言查询和相关性排序。
- **Docker 增强**: 索引在容器启动时自动构建，无需手动配置，完美支持 Docker 环境。

## [1.0.1] - 2025-12-19

### 优化 (Optimizations)
- **代码重构**: 提取通用的目录扫描逻辑到 `_scan_directory_docs` 函数，消除了 `search_platform_docs` 中针对 SDK/UIKit/CallKit 的重复代码。
- **性能提升**: 引入 `asyncio.to_thread` 将阻塞的文件 I/O 操作（`os.walk`, `open`）放入线程池执行，实现真正的非阻塞调用。
- **缓存机制**: 为文档扫描结果添加 `lru_cache`，减少频繁请求时的重复文件系统遍历。
- **依赖更新**: 明确项目最低 Python 版本要求为 3.9+ (因为使用了 `asyncio.to_thread`)。

### 作者
- AI Assistant
