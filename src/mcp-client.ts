import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import EasemobDocSearchClient from './client';

// 创建MCP客户端
const client = new Client({
  name: 'easemob-doc-search-client',
  version: '1.0.0',
});

// 创建文档搜索客户端
const docSearchClient = new EasemobDocSearchClient({
  baseUrl: process.env.EASEMOB_API_URL || 'http://localhost:8000'
});

// 注册工具
client.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case 'search_platform_docs': {
      const { platform } = args as { platform: string };
      
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
        const result = await docSearchClient.getDocContent(doc_path, keyword);
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

    case 'search_docs_stream': {
      const { platform } = args as { platform: string };
      
      if (!platform) {
        throw new Error('platform参数是必需的');
      }

      try {
        const stream = docSearchClient.searchDocsStream(platform);
        const events = [];
        
        for await (const event of stream) {
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
      } catch (error) {
        throw new Error(`流式搜索文档失败: ${error}`);
      }
    }

    case 'get_doc_content_stream': {
      const { doc_path, keyword = '' } = args as { doc_path: string; keyword?: string };
      
      if (!doc_path) {
        throw new Error('doc_path参数是必需的');
      }

      try {
        const stream = docSearchClient.getDocContentStream(doc_path, keyword);
        const events = [];
        
        for await (const event of stream) {
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
      } catch (error) {
        throw new Error(`流式获取文档内容失败: ${error}`);
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
      } catch (error) {
        throw new Error(`健康检查失败: ${error}`);
      }
    }

    default:
      throw new Error(`未知的工具: ${name}`);
  }
});

// 启动MCP客户端
async function main() {
  const transport = new StdioClientTransport();
  await client.connect(transport);
  console.error('MCP客户端已启动，连接到远程API服务');
}

main().catch(console.error); 