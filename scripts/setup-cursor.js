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

  console.log('请选择部署方式:');
  console.log('1. 本地部署 (localhost)');
  console.log('2. 远程服务器部署 (Docker/云服务器)');
  console.log('3. 内网部署');
  console.log('4. 生产环境部署 (HTTPS)');

  rl.question('请选择 (1-4): ', (choice) => {
    switch (choice) {
      case '1':
        setupLocalConfig(rl);
        break;
      case '2':
        setupRemoteConfig(rl);
        break;
      case '3':
        setupInternalConfig(rl);
        break;
      case '4':
        setupProductionConfig(rl);
        break;
      default:
        console.log('无效选择，使用本地配置');
        setupLocalConfig(rl);
    }
  });
}

/**
 * 本地部署配置
 */
function setupLocalConfig(rl) {
  rl.question('请输入本地服务器端口 (默认: 8000): ', (port) => {
    const serverUrl = `http://localhost:${port || 8000}`;
    const projectPath = process.cwd();
    
    const config = generateLocalConfig(serverUrl, projectPath);
    saveConfig(config, '本地部署');
    rl.close();
  });
}

/**
 * 远程服务器配置
 */
function setupRemoteConfig(rl) {
  rl.question('请输入远程服务器地址 (例如: http://your-server.com:8000): ', (serverUrl) => {
    if (!serverUrl) {
      console.log('❌ 服务器地址不能为空');
      rl.close();
      return;
    }
    
    const config = generateRemoteConfig(serverUrl);
    saveConfig(config, '远程服务器部署');
    generateEnvFile(serverUrl);
    rl.close();
  });
}

/**
 * 内网部署配置
 */
function setupInternalConfig(rl) {
  rl.question('请输入内网服务器IP和端口 (例如: 192.168.1.100:8000): ', (serverInfo) => {
    if (!serverInfo) {
      console.log('❌ 服务器信息不能为空');
      rl.close();
      return;
    }
    
    const serverUrl = `http://${serverInfo}`;
    const config = generateRemoteConfig(serverUrl);
    saveConfig(config, '内网部署');
    generateEnvFile(serverUrl);
    rl.close();
  });
}

/**
 * 生产环境配置
 */
function setupProductionConfig(rl) {
  rl.question('请输入生产服务器域名 (例如: https://your-domain.com): ', (domain) => {
    if (!domain) {
      console.log('❌ 域名不能为空');
      rl.close();
      return;
    }
    
    const serverUrl = domain.startsWith('http') ? domain : `https://${domain}`;
    const config = generateRemoteConfig(serverUrl);
    saveConfig(config, '生产环境部署');
    generateEnvFile(serverUrl);
    rl.close();
  });
}

/**
 * 生成本地配置
 */
function generateLocalConfig(serverUrl, projectPath) {
  return {
    "mcpServers": {
      "easemob-docs": {
        "command": "node",
        "args": [path.join(projectPath, "dist", "mcp-server.js")],
        "env": {
          "NODE_ENV": "production"
        },
        "description": "环信文档搜索服务 - 本地部署"
      }
    }
  };
}

/**
 * 生成远程配置
 */
function generateRemoteConfig(serverUrl) {
  return {
    "mcpServers": {
      "easemob-docs": {
        "command": "npx",
        "args": ["@easemob/docs-mcp@latest", "mcp-remote"],
        "env": {
          "EASEMOB_API_URL": serverUrl,
          "NODE_ENV": "production"
        },
        "description": "环信文档搜索服务 - 远程部署"
      }
    }
  };
}

/**
 * 保存配置
 */
function saveConfig(config, type) {
  // 显示配置
  console.log(`\n📋 生成的${type}配置:`);
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
  
  // 显示Docker部署说明
  if (type !== '本地部署') {
    console.log('\n🐳 Docker部署说明:');
    console.log('1. 在服务器上运行: docker-compose up -d');
    console.log('2. 确保服务器地址可以访问');
    console.log('3. 测试连接: curl ' + config.mcpServers['easemob-docs'].env.EASEMOB_API_URL + '/health');
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
## 📝 使用示例

在Cursor中，你可以这样使用：

1. 搜索文档：
   "请帮我搜索 Android 平台的文档"

2. 获取文档内容：
   "请获取 android/quickstart.md 的内容"

3. 获取可用平台：
   "有哪些可用的平台？"

4. 获取统计信息：
   "显示文档统计信息"
`;

  const examplesPath = path.join(process.cwd(), 'cursor-usage-examples.md');
  fs.writeFileSync(examplesPath, examples);
  
  console.log(`\n📖 使用示例已生成: ${examplesPath}`);
}

// 运行设置
if (require.main === module) {
  setupCursorConfig();
}

module.exports = { setupCursorConfig }; 