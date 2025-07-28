import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { DocSearchService } from './services/doc-search.service';

// 创建MCP服务器
const server = new Server(
  {
    name: 'easemob-doc-search',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 创建文档搜索服务实例
const docSearchService = new DocSearchService();

// 注册工具：搜索平台文档
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case 'search_platform_docs': {
      const { platform } = args as { platform: string };
      
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
      } catch (error) {
        throw new Error(`搜索文档失败: ${error}`);
      }
    }

    case 'get_document_content': {
      const { doc_path, keyword = '' } = args as { doc_path: string; keyword?: string };
      
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
      } catch (error) {
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
      } catch (error) {
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
      } catch (error) {
        throw new Error(`获取文档统计失败: ${error}`);
      }
    }

    default:
      throw new Error(`未知的工具: ${name}`);
  }
});

// 启动MCP服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('MCP服务器已启动');
}

main().catch(console.error); 