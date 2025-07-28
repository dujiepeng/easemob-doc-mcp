#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const index_js_1 = require("@modelcontextprotocol/sdk/server/index.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const doc_search_service_1 = require("./services/doc-search.service");
// 创建MCP服务器
const server = new index_js_1.Server({
    name: 'easemob-doc-search',
    version: '1.0.0',
});
// 创建文档搜索服务实例
const docSearchService = new doc_search_service_1.DocSearchService();
// 注册工具：搜索平台文档
server.setRequestHandler('tools/call', async (request) => {
    const { name, arguments: args } = request.params;
    switch (name) {
        case 'search_platform_docs': {
            const { platform } = args;
            if (!platform) {
                throw new Error('platform参数是必需的');
            }
            try {
                const results = await docSearchService.searchPlatformDocs(platform);
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
                const result = await docSearchService.getDocumentContent(doc_path, keyword);
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
        case 'get_available_platforms': {
            try {
                const platforms = await docSearchService.getAvailablePlatforms();
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
                const stats = await docSearchService.getDocumentStats();
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
// 启动MCP服务器
async function main() {
    const transport = new stdio_js_1.StdioServerTransport();
    await server.connect(transport);
    console.error('MCP服务器已启动');
}
main().catch(console.error);
//# sourceMappingURL=mcp-server.js.map