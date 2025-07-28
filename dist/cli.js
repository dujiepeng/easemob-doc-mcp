#!/usr/bin/env node
"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const commander_1 = require("commander");
const client_1 = __importDefault(require("./client"));
const child_process_1 = require("child_process");
const path = __importStar(require("path"));
const program = new commander_1.Command();
program
    .name('@easemob/docs-mcp')
    .description('环信文档搜索服务 - MCP服务器和CLI工具')
    .version('1.0.0');
// 搜索文档命令
program
    .command('search')
    .description('搜索平台文档')
    .argument('<platform>', '平台名称 (android, ios, web, flutter等)')
    .option('-u, --url <url>', 'API服务器地址', 'http://localhost:8000')
    .action(async (platform, options) => {
    try {
        const client = new client_1.default({ baseUrl: options.url });
        const result = await client.searchDocs(platform);
        console.log(`找到 ${result.results.length} 个文档:`);
        result.results.forEach((doc) => {
            console.log(`- ${doc.path} (${doc.platform})`);
        });
    }
    catch (error) {
        console.error('搜索失败:', error);
        process.exit(1);
    }
});
// 获取文档内容命令
program
    .command('content')
    .description('获取文档内容')
    .argument('<path>', '文档路径')
    .option('-u, --url <url>', 'API服务器地址', 'http://localhost:8000')
    .option('-k, --keyword <keyword>', '搜索关键词')
    .action(async (docPath, options) => {
    try {
        const client = new client_1.default({ baseUrl: options.url });
        const result = await client.getDocContent(docPath, { keyword: options.keyword });
        console.log('文档内容:');
        console.log(result.content);
    }
    catch (error) {
        console.error('获取内容失败:', error);
        process.exit(1);
    }
});
// 健康检查命令
program
    .command('health')
    .description('检查服务健康状态')
    .option('-u, --url <url>', 'API服务器地址', 'http://localhost:8000')
    .action(async (options) => {
    try {
        const client = new client_1.default({ baseUrl: options.url });
        const health = await client.healthCheck();
        console.log('服务状态:', health);
    }
    catch (error) {
        console.error('健康检查失败:', error);
        process.exit(1);
    }
});
// 启动服务器命令
program
    .command('serve')
    .description('启动文档搜索服务器')
    .option('-p, --port <port>', '服务器端口', '8000')
    .option('-m, --mode <mode>', '运行模式 (api|mcp|both)', 'api')
    .action(async (options) => {
    console.log('🚀 启动环信文档搜索服务器...');
    try {
        const serverScript = path.join(__dirname, 'server.js');
        if (options.mode === 'api' || options.mode === 'both') {
            const apiProcess = (0, child_process_1.spawn)('node', [serverScript], {
                stdio: 'inherit',
                env: { ...process.env, PORT: options.port }
            });
            apiProcess.on('error', (error) => {
                console.error('API服务器启动失败:', error);
                process.exit(1);
            });
            console.log(`✅ API服务器已启动，端口: ${options.port}`);
        }
        if (options.mode === 'mcp' || options.mode === 'both') {
            const mcpScript = path.join(__dirname, 'mcp-server.js');
            const mcpProcess = (0, child_process_1.spawn)('node', [mcpScript], {
                stdio: 'inherit'
            });
            mcpProcess.on('error', (error) => {
                console.error('MCP服务器启动失败:', error);
                process.exit(1);
            });
            console.log('✅ MCP服务器已启动');
        }
    }
    catch (error) {
        console.error('服务器启动失败:', error);
        process.exit(1);
    }
});
// 统计信息命令
program
    .command('stats')
    .description('获取文档统计信息')
    .option('-u, --url <url>', 'API服务器地址', 'http://localhost:8000')
    .action(async (options) => {
    try {
        const client = new client_1.default({ baseUrl: options.url });
        const stats = await client.getDocumentStats();
        console.log('文档统计信息:');
        console.log(JSON.stringify(stats, null, 2));
    }
    catch (error) {
        console.error('获取统计信息失败:', error);
        process.exit(1);
    }
});
// 流式搜索命令
program
    .command('stream-search')
    .description('流式搜索文档')
    .argument('<platform>', '平台名称')
    .option('-u, --url <url>', 'API服务器地址', 'http://localhost:8000')
    .action(async (platform, options) => {
    try {
        const client = new client_1.default({ baseUrl: options.url });
        console.log(`开始流式搜索 ${platform} 文档...`);
        for await (const event of client.searchDocsStream(platform)) {
            switch (event.type) {
                case 'start':
                    console.log('🚀 开始搜索...');
                    break;
                case 'progress':
                    console.log(`📊 进度: ${event.message}`);
                    break;
                case 'results_batch':
                    console.log(`📄 找到 ${event.data?.length || 0} 个文档`);
                    break;
                case 'complete':
                    console.log('✅ 搜索完成');
                    break;
                case 'error':
                    console.error('❌ 搜索错误:', event.message);
                    break;
            }
        }
    }
    catch (error) {
        console.error('流式搜索失败:', error);
        process.exit(1);
    }
});
// 如果没有提供命令，显示帮助
if (process.argv.length === 2) {
    program.help();
}
program.parse();
//# sourceMappingURL=cli.js.map