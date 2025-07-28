#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * 设置Cursor的MCP配置
 */
function setupCursorConfig() {
  console.log('🔧 设置Cursor MCP配置...\n');

  // 获取用户输入
  const readline = require('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  rl.question('请输入你的服务器URL (例如: http://localhost:8000 或 https://your-server.com): ', (serverUrl) => {
    rl.question('请输入项目路径 (例如: /path/to/easemob-doc-search): ', (projectPath) => {
      rl.close();
      
      // 生成配置
      const config = generateCursorConfig(serverUrl, projectPath);
      
      // 显示配置
      console.log('\n📋 生成的Cursor配置:');
      console.log('='.repeat(50));
      console.log(JSON.stringify(config, null, 2));
      console.log('='.repeat(50));
      
      // 保存配置文件
      const configPath = path.join(process.cwd(), 'cursor-mcp-config.json');
      fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
      
      console.log(`\n✅ 配置已保存到: ${configPath}`);
      console.log('\n📝 使用说明:');
      console.log('1. 打开Cursor设置');
      console.log('2. 找到MCP配置部分');
      console.log('3. 将上述配置复制到MCP设置中');
      console.log('4. 重启Cursor');
      
      // 生成环境变量文件
      generateEnvFile(serverUrl);
    });
  });
}

/**
 * 生成Cursor MCP配置
 */
function generateCursorConfig(serverUrl, projectPath) {
  const isLocal = serverUrl.includes('localhost') || serverUrl.includes('127.0.0.1');
  
  if (isLocal) {
    // 本地部署 - 直接使用MCP服务器
    return {
      "mcpServers": {
        "easemob-docs": {
          "command": "node",
          "args": [path.join(projectPath, "dist", "mcp-server.js")],
          "env": {
            "NODE_ENV": "production"
          },
          "description": "环信文档搜索服务 - 按平台搜索文档并获取内容"
        }
      }
    };
  } else {
    // 远程部署 - 使用MCP客户端连接到远程API
    return {
      "mcpServers": {
        "easemob-docs": {
          "command": "node",
          "args": [path.join(projectPath, "dist", "mcp-client.js")],
          "env": {
            "NODE_ENV": "production",
            "EASEMOB_API_URL": serverUrl
          },
          "description": "环信文档搜索服务 - 连接到远程API服务"
        }
      }
    };
  }
}

/**
 * 生成环境变量文件
 */
function generateEnvFile(serverUrl) {
  const envContent = `# 环信文档搜索服务环境变量
EASEMOB_API_URL=${serverUrl}
NODE_ENV=production
`;
  
  const envPath = path.join(process.cwd(), '.env');
  fs.writeFileSync(envPath, envContent);
  
  console.log(`\n📄 环境变量文件已生成: ${envPath}`);
}

/**
 * 生成使用示例
 */
function generateUsageExamples() {
  const examples = `
## 🚀 在Cursor中使用示例

### 1. 搜索Android平台文档
\`\`\`javascript
// 搜索Android平台的所有文档
const docs = await mcp.call("search_platform_docs", {"platform": "android"});
console.log('找到的文档:', docs);
\`\`\`

### 2. 获取文档内容
\`\`\`javascript
// 获取特定文档的内容
const content = await mcp.call("get_document_content", {
  "doc_path": "android/overview.md"
});
console.log('文档内容:', content);
\`\`\`

### 3. 在文档中搜索关键字
\`\`\`javascript
// 在文档中搜索"初始化"关键字
const results = await mcp.call("get_document_content", {
  "doc_path": "android/overview.md", 
  "keyword": "初始化"
});
console.log('搜索结果:', results);
\`\`\`

### 4. 流式搜索文档
\`\`\`javascript
// 流式搜索iOS平台文档
const streamResults = await mcp.call("search_docs_stream", {"platform": "ios"});
console.log('流式搜索结果:', streamResults);
\`\`\`

### 5. 健康检查
\`\`\`javascript
// 检查服务状态
const health = await mcp.call("health_check", {});
console.log('服务状态:', health);
\`\`\`
`;

  const examplesPath = path.join(process.cwd(), 'CURSOR_USAGE_EXAMPLES.md');
  fs.writeFileSync(examplesPath, examples);
  
  console.log(`\n📚 使用示例已生成: ${examplesPath}`);
}

// 运行设置
if (require.main === module) {
  setupCursorConfig();
  generateUsageExamples();
}

module.exports = { setupCursorConfig, generateCursorConfig }; 