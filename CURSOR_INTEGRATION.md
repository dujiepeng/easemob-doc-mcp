# Cursor集成指南

本指南详细介绍如何将环信文档搜索服务集成到Cursor编辑器中。

## 🚀 快速配置

### 方法一：使用npx（推荐）

这是最简单的方法，无需本地安装：

```json
{
  "easemob-docs": {
    "command": "npx",
    "args": ["@easemob/docs-mcp@latest"]
  }
}
```

### 方法二：本地安装

如果你已经安装了包：

```json
{
  "easemob-docs": {
    "command": "easemob-doc-search",
    "args": ["mcp"]
  }
}
```

### 方法三：直接路径

如果你有本地构建的文件：

```json
{
  "easemob-docs": {
    "command": "node",
    "args": ["/path/to/dist/mcp-server.js"]
  }
}
```

## 📋 完整配置示例

在你的Cursor MCP配置文件（通常是 `~/.cursor/mcp.json`）中添加：

```json
{
  "mcpServers": {
    "easemob-docs": {
      "command": "npx",
      "args": ["@easemob/docs-mcp@latest"],
      "description": "环信文档搜索服务 - 支持多平台文档搜索和内容获取"
    }
  }
}
```

## 🛠️ 自动配置脚本

我们提供了一个自动配置脚本：

```bash
# 运行配置脚本
npx @easemob/docs-mcp@latest setup-cursor
```

这个脚本会：
1. 检测你的系统环境
2. 生成合适的MCP配置
3. 创建使用示例文档

## 🔧 可用的MCP工具

### 1. 搜索平台文档

**工具名**: `search_platform_docs`

**描述**: 搜索指定平台的文档列表

**参数**:
- `platform` (string, 必需): 平台名称，如 "android", "ios", "web", "flutter" 等

**示例**:
```javascript
// 搜索Android平台文档
const result = await mcp.call("search_platform_docs", {
  "platform": "android"
});

// 搜索iOS平台文档
const result = await mcp.call("search_platform_docs", {
  "platform": "ios"
});
```

### 2. 获取文档内容

**工具名**: `get_document_content`

**描述**: 获取指定文档的内容，支持关键字搜索

**参数**:
- `doc_path` (string, 必需): 文档路径，如 "android/quickstart.md"
- `keyword` (string, 可选): 搜索关键字

**示例**:
```javascript
// 获取文档完整内容
const result = await mcp.call("get_document_content", {
  "doc_path": "android/quickstart.md"
});

// 在文档中搜索关键字
const result = await mcp.call("get_document_content", {
  "doc_path": "android/quickstart.md",
  "keyword": "初始化"
});
```

### 3. 获取可用平台列表

**工具名**: `get_available_platforms`

**描述**: 获取所有可用的文档平台列表

**参数**: 无

**示例**:
```javascript
const platforms = await mcp.call("get_available_platforms", {});
console.log("可用平台:", platforms);
```

### 4. 获取文档统计信息

**工具名**: `get_document_stats`

**描述**: 获取文档库的统计信息

**参数**: 无

**示例**:
```javascript
const stats = await mcp.call("get_document_stats", {});
console.log("文档统计:", stats);
```

## 📖 使用场景

### 1. 快速查找API文档

```javascript
// 查找Android平台的API文档
const androidDocs = await mcp.call("search_platform_docs", {
  "platform": "android"
});

// 获取特定API文档内容
const apiDoc = await mcp.call("get_document_content", {
  "doc_path": "android/apireference.md"
});
```

### 2. 搜索特定功能

```javascript
// 在所有Android文档中搜索"登录"相关内容
const loginDocs = await mcp.call("search_platform_docs", {
  "platform": "android"
});

// 在登录文档中搜索具体实现
const loginContent = await mcp.call("get_document_content", {
  "doc_path": "android/login.md",
  "keyword": "登录"
});
```

### 3. 跨平台对比

```javascript
// 获取多个平台的相同功能文档
const platforms = ["android", "ios", "flutter"];
const results = {};

for (const platform of platforms) {
  const docs = await mcp.call("search_platform_docs", {
    "platform": platform
  });
  results[platform] = docs;
}
```

## 🌐 支持的平台

- **Android**: Android SDK文档
- **iOS**: iOS SDK文档
- **Web**: Web SDK文档
- **Flutter**: Flutter SDK文档
- **React Native**: React Native SDK文档
- **Unity**: Unity SDK文档
- **Electron**: Electron SDK文档
- **HarmonyOS**: HarmonyOS SDK文档
- **小程序**: 各种小程序平台文档
- **服务端**: 服务端API文档

## 🔍 故障排除

### 1. 工具未找到

**问题**: Cursor提示找不到MCP工具

**解决方案**:
1. 检查MCP配置文件是否正确
2. 确保npx命令可用
3. 尝试重新启动Cursor

### 2. 连接失败

**问题**: 无法连接到MCP服务器

**解决方案**:
1. 检查网络连接
2. 确认包名是否正确
3. 尝试手动安装包：`npm install -g @easemob/docs-mcp`

### 3. 权限问题

**问题**: 执行权限被拒绝

**解决方案**:
```bash
# 重新安装包
npm uninstall -g @easemob/docs-mcp
npm install -g @easemob/docs-mcp

# 或者使用npx
npx @easemob/docs-mcp@latest
```

### 4. 版本兼容性

**问题**: 版本不兼容

**解决方案**:
1. 更新到最新版本
2. 检查Node.js版本（需要16+）
3. 清除缓存：`npm cache clean --force`

## 🐛 调试

### 启用调试模式

在MCP配置中添加环境变量：

```json
{
  "easemob-docs": {
    "command": "npx",
    "args": ["@easemob/docs-mcp@latest"],
    "env": {
      "DEBUG": "easemob-docs:*"
    }
  }
}
```

### 查看日志

```bash
# 直接运行查看输出
npx @easemob/docs-mcp@latest

# 或者查看Cursor的日志
# 在Cursor中打开开发者工具查看控制台输出
```

## 📚 更多资源

- [Model Context Protocol 官方文档](https://modelcontextprotocol.io/)
- [Cursor MCP 集成指南](https://cursor.sh/docs/mcp)
- [环信官方文档](https://docs.easemob.com/)
- [项目GitHub仓库](https://github.com/easemob/easemob-doc-search)

## 🤝 获取帮助

如果你遇到问题：

1. 查看本指南的故障排除部分
2. 检查项目的GitHub Issues
3. 提交新的Issue描述你的问题
4. 联系环信技术支持

---

**注意**: 确保你的Cursor版本支持MCP功能。如果遇到兼容性问题，请更新到最新版本的Cursor。 