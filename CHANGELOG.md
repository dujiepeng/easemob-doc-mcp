# Changelog

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
