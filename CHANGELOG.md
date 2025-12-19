# Changelog

## [1.0.1] - 2025-12-19

### 优化 (Optimizations)
- **代码重构**: 提取通用的目录扫描逻辑到 `_scan_directory_docs` 函数，消除了 `search_platform_docs` 中针对 SDK/UIKit/CallKit 的重复代码。
- **性能提升**: 引入 `asyncio.to_thread` 将阻塞的文件 I/O 操作（`os.walk`, `open`）放入线程池执行，实现真正的非阻塞调用。
- **缓存机制**: 为文档扫描结果添加 `lru_cache`，减少频繁请求时的重复文件系统遍历。
- **依赖更新**: 明确项目最低 Python 版本要求为 3.9+ (因为使用了 `asyncio.to_thread`)。

### 作者
- AI Assistant
