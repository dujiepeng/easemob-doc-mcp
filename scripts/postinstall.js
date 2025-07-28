#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * Post-install 脚本
 * 确保MCP服务器文件有正确的执行权限
 */
function postinstall() {
  console.log('🔧 设置环信文档搜索MCP服务器...');

  try {
    // 获取当前包的根目录
    const packageRoot = path.resolve(__dirname, '..');
    const mcpServerPath = path.join(packageRoot, 'dist', 'mcp-server.js');
    const cliPath = path.join(packageRoot, 'dist', 'cli.js');

    // 检查文件是否存在
    if (fs.existsSync(mcpServerPath)) {
      // 设置执行权限
      fs.chmodSync(mcpServerPath, '755');
      console.log('✅ MCP服务器文件权限设置完成');
    } else {
      console.log('⚠️  MCP服务器文件不存在，请先运行 npm run build');
    }

    if (fs.existsSync(cliPath)) {
      // 设置执行权限
      fs.chmodSync(cliPath, '755');
      console.log('✅ CLI工具文件权限设置完成');
    }

    console.log('\n📋 使用说明:');
    console.log('1. 在Cursor中配置MCP服务器:');
    console.log('   {');
    console.log('     "easemob-docs": {');
    console.log('       "command": "npx",');
    console.log('       "args": ["@easemob/docs-mcp@latest"]');
    console.log('     }');
    console.log('   }');
    console.log('\n2. 或者直接使用:');
    console.log('   npx @easemob/docs-mcp@latest');
    console.log('\n3. 查看帮助:');
    console.log('   npx @easemob/docs-mcp@latest --help');

  } catch (error) {
    console.error('❌ Post-install 失败:', error.message);
    process.exit(1);
  }
}

// 运行 postinstall
if (require.main === module) {
  postinstall();
}

module.exports = { postinstall }; 