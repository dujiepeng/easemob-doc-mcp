# Cursor集成指南

本指南详细说明如何在Cursor中使用部署后的环信文档搜索服务。

## 🚀 快速开始

### 1. 自动配置（推荐）

运行配置脚本，自动生成Cursor配置：

```bash
# 构建项目
npm run build

# 运行配置脚本
npm run setup-cursor
```

脚本会提示你输入：
- 服务器URL（本地或远程）
- 项目路径

然后自动生成配置文件。

### 2. 手动配置

#### 本地部署配置

如果服务部署在本地：

```json
{
  "mcpServers": {
    "easemob-docs": {
      "command": "node",
      "args": ["/path/to/easemob-doc-search/dist/mcp-server.js"],
      "env": {
        "NODE_ENV": "production"
      },
      "description": "环信文档搜索服务 - 按平台搜索文档并获取内容"
    }
  }
}
```

#### 远程部署配置

如果服务部署在远程服务器：

```json
{
  "mcpServers": {
    "easemob-docs": {
      "command": "node",
      "args": ["/path/to/easemob-doc-search/dist/mcp-client.js"],
      "env": {
        "NODE_ENV": "production",
        "EASEMOB_API_URL": "https://your-server.com"
      },
      "description": "环信文档搜索服务 - 连接到远程API服务"
    }
  }
}
```

## 🔧 配置步骤

### 1. 打开Cursor设置

- 打开Cursor
- 按 `Cmd/Ctrl + ,` 打开设置
- 搜索 "MCP" 或 "Model Context Protocol"

### 2. 添加MCP服务器配置

在MCP配置部分添加上述JSON配置。

### 3. 重启Cursor

配置完成后重启Cursor以加载新的MCP服务器。

### 4. 验证连接

在Cursor中打开聊天，输入：

```
请帮我搜索Android平台的文档
```

如果配置正确，你应该能看到搜索结果。

## 📚 可用工具

### 1. 搜索平台文档

```javascript
// 搜索指定平台的所有文档
const docs = await mcp.call("search_platform_docs", {
  "platform": "android"  // 或 "ios", "web", "flutter" 等
});
```

### 2. 获取文档内容

```javascript
// 获取特定文档的完整内容
const content = await mcp.call("get_document_content", {
  "doc_path": "android/overview.md"
});
```

### 3. 在文档中搜索关键字

```javascript
// 在文档中搜索特定关键字
const results = await mcp.call("get_document_content", {
  "doc_path": "android/overview.md",
  "keyword": "初始化"
});
```

### 4. 流式搜索文档

```javascript
// 流式搜索文档（返回所有SSE事件）
const streamResults = await mcp.call("search_docs_stream", {
  "platform": "ios"
});
```

### 5. 流式获取文档内容

```javascript
// 流式获取文档内容（返回所有SSE事件）
const contentStream = await mcp.call("get_doc_content_stream", {
  "doc_path": "android/overview.md",
  "keyword": "初始化"
});
```

### 6. 健康检查

```javascript
// 检查服务状态
const health = await mcp.call("health_check", {});
```

## 🎯 使用场景

### 场景1：快速查找API文档

```
用户：我需要Android平台的登录API文档
AI：我来帮你搜索Android平台的登录相关文档...
```

### 场景2：查找特定功能

```
用户：如何在iOS中实现消息发送？
AI：让我搜索iOS平台的消息发送相关文档...
```

### 场景3：获取代码示例

```
用户：给我一个Flutter的初始化代码示例
AI：我来查找Flutter平台的初始化文档...
```

## 🔍 支持的平台

- **android** - Android平台文档
- **ios** - iOS平台文档
- **web** - Web平台文档
- **flutter** - Flutter平台文档
- **react-native** - React Native平台文档
- **unity** - Unity平台文档
- **electron** - Electron平台文档
- **harmonyos** - 鸿蒙平台文档
- **applet** - 小程序平台文档
- **server-side** - 服务端文档

## 🛠️ 故障排除

### 问题1：MCP服务器连接失败

**症状：** Cursor显示MCP服务器连接错误

**解决方案：**
1. 检查服务器是否正在运行
2. 验证配置文件中的路径是否正确
3. 确保Node.js版本 >= 16
4. 检查环境变量设置

### 问题2：找不到文档

**症状：** 搜索返回空结果

**解决方案：**
1. 确认文档目录存在且包含.md文件
2. 检查平台名称是否正确
3. 验证文档路径格式

### 问题3：权限错误

**症状：** 文件访问权限错误

**解决方案：**
1. 确保文档目录有读取权限
2. 检查Node.js进程权限
3. 在Docker中运行时检查卷挂载

### 问题4：网络连接问题

**症状：** 远程API连接失败

**解决方案：**
1. 检查网络连接
2. 验证服务器URL是否正确
3. 确认防火墙设置
4. 检查CORS配置

## 📝 调试技巧

### 1. 启用详细日志

设置环境变量：
```bash
export DEBUG=easemob-doc-search:*
```

### 2. 测试API端点

```bash
# 健康检查
curl http://localhost:8000/health

# 搜索文档
curl "http://localhost:8000/api/search-docs?platform=android"

# 获取文档内容
curl "http://localhost:8000/api/get-doc-content?path=android/overview.md"
```

### 3. 查看MCP日志

在Cursor中查看MCP服务器的输出日志，通常包含详细的错误信息。

## 🔄 更新配置

当服务器地址或路径发生变化时：

1. 更新Cursor的MCP配置
2. 重启Cursor
3. 测试连接

或者重新运行配置脚本：
```bash
npm run setup-cursor
```

## 📞 获取帮助

如果遇到问题：

1. 查看 [GitHub Issues](https://github.com/easemob/easemob-doc-search/issues)
2. 提交新的Issue
3. 联系技术支持团队

## 🎉 成功标志

配置成功后，你应该能够：

1. 在Cursor中正常使用文档搜索功能
2. 看到准确的搜索结果
3. 获取完整的文档内容
4. 进行关键字搜索
5. 使用流式搜索功能 