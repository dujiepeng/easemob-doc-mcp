#!/usr/bin/env node
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const index_js_1 = require("@modelcontextprotocol/sdk/client/index.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/client/stdio.js");
const client_1 = __importDefault(require("./client"));
const client = new index_js_1.Client({
    name: 'easemob-doc-search-client',
    version: '1.0.0',
});
const docSearchClient = new client_1.default({
    baseUrl: process.env.EASEMOB_API_URL || 'http://localhost:8000'
});
client.setRequestHandler('tools/call', async (request) => {
    const { name, arguments: args } = request.params;
    switch (name) {
        case 'search_platform_docs': {
            const { platform } = args;
            if (!platform) {
                throw new Error('platform参数是必需的');
            }
            try {
                const results = await docSearchClient.searchDocs(platform);
                return {
                    content: [
                        {
                            type: 'text',
                            text: JSON.stringify(results, null, 2)
                        }
                    ]
                };
            }
            catch (error) {
                throw new Error(`搜索文档失败: ${error}`);
            }
        }
        case 'get_document_content': {
            const { doc_path, keyword = '' } = args;
            if (!doc_path) {
                throw new Error('doc_path参数是必需的');
            }
            try {
                const result = await docSearchClient.getDocContent(doc_path, { keyword });
                return {
                    content: [
                        {
                            type: 'text',
                            text: JSON.stringify(result, null, 2)
                        }
                    ]
                };
            }
            catch (error) {
                throw new Error(`获取文档内容失败: ${error}`);
            }
        }
        case 'search_docs_stream': {
            const { platform } = args;
            if (!platform) {
                throw new Error('platform参数是必需的');
            }
            try {
                const events = [];
                for await (const event of docSearchClient.searchDocsStream(platform)) {
                    events.push(event);
                }
                return {
                    content: [
                        {
                            type: 'text',
                            text: JSON.stringify(events, null, 2)
                        }
                    ]
                };
            }
            catch (error) {
                throw new Error(`流式搜索失败: ${error}`);
            }
        }
        case 'get_doc_content_stream': {
            const { doc_path, keyword = '' } = args;
            if (!doc_path) {
                throw new Error('doc_path参数是必需的');
            }
            try {
                const events = [];
                for await (const event of docSearchClient.getDocContentStream(doc_path, keyword)) {
                    events.push(event);
                }
                return {
                    content: [
                        {
                            type: 'text',
                            text: JSON.stringify(events, null, 2)
                        }
                    ]
                };
            }
            catch (error) {
                throw new Error(`流式获取内容失败: ${error}`);
            }
        }
        case 'health_check': {
            try {
                const health = await docSearchClient.healthCheck();
                return {
                    content: [
                        {
                            type: 'text',
                            text: JSON.stringify(health, null, 2)
                        }
                    ]
                };
            }
            catch (error) {
                throw new Error(`健康检查失败: ${error}`);
            }
        }
        case 'get_available_platforms': {
            try {
                // 这里需要实现获取平台列表的逻辑
                const platforms = ['android', 'ios', 'web', 'flutter', 'react-native', 'unity', 'electron', 'harmonyos', 'applet', 'server-side'];
                return {
                    content: [
                        {
                            type: 'text',
                            text: JSON.stringify(platforms, null, 2)
                        }
                    ]
                };
            }
            catch (error) {
                throw new Error(`获取平台列表失败: ${error}`);
            }
        }
        case 'get_document_stats': {
            try {
                const stats = await docSearchClient.getDocumentStats();
                return {
                    content: [
                        {
                            type: 'text',
                            text: JSON.stringify(stats, null, 2)
                        }
                    ]
                };
            }
            catch (error) {
                throw new Error(`获取文档统计失败: ${error}`);
            }
        }
        default:
            throw new Error(`未知的工具: ${name}`);
    }
});
async function main() {
    const transport = new stdio_js_1.StdioClientTransport({
        command: 'node',
        args: ['dist/mcp-client.js']
    });
    await client.connect(transport);
    console.error('MCP客户端已启动');
}
main().catch(console.error);
//# sourceMappingURL=mcp-client.js.map