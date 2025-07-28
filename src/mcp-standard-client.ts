#!/usr/bin/env node

import EasemobDocSearchClient from './client';

// 从环境变量获取远程服务器URL
const remoteUrl = process.env.EASEMOB_API_URL || 'http://localhost:8000';
const docSearchClient = new EasemobDocSearchClient({
  baseUrl: remoteUrl
});

console.error(`🔗 连接到远程服务器: ${remoteUrl}`);

// 定义可用的工具
const tools = [
  {
    name: 'search_platform_docs',
    description: '搜索指定平台的文档列表',
    inputSchema: {
      type: 'object',
      properties: {
        platform: {
          type: 'string',
          description: '平台名称 (android, ios, web, flutter等)'
        }
      },
      required: ['platform']
    }
  },
  {
    name: 'get_document_content',
    description: '获取指定文档的内容',
    inputSchema: {
      type: 'object',
      properties: {
        doc_path: {
          type: 'string',
          description: '文档路径'
        },
        keyword: {
          type: 'string',
          description: '搜索关键词（可选）'
        }
      },
      required: ['doc_path']
    }
  },
  {
    name: 'get_document_stats',
    description: '获取文档统计信息',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  },
  {
    name: 'get_available_platforms',
    description: '获取可用的平台列表',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  }
];

// 标准 MCP 协议实现
async function handleMCPRequest() {
  const stdin = process.stdin;
  const stdout = process.stdout;
  
  stdin.setEncoding('utf8');
  
  stdin.on('data', async (data) => {
    try {
      const lines = data.toString().split('\n');
      
      for (const line of lines) {
        if (line.trim() === '') continue;
        
        const request = JSON.parse(line);
        
        if (request.method === 'initialize') {
          // 响应初始化请求
          const response = {
            jsonrpc: '2.0',
            id: request.id,
            result: {
              protocolVersion: '2024-11-05',
              capabilities: {
                tools: {}
              },
              serverInfo: {
                name: 'easemob-doc-search-client',
                version: '1.0.0'
              }
            }
          };
          stdout.write(JSON.stringify(response) + '\n');
        } else if (request.method === 'tools/list') {
          // 响应工具列表请求
          const response = {
            jsonrpc: '2.0',
            id: request.id,
            result: {
              tools: tools
            }
          };
          stdout.write(JSON.stringify(response) + '\n');
        } else if (request.method === 'tools/call') {
          // 处理工具调用
          const { name, arguments: args } = request.params;
          
          console.error(`🔧 调用工具: ${name}, 参数:`, args);
          
          try {
            let result;
            
            switch (name) {
              case 'search_platform_docs': {
                const { platform } = args;
                if (!platform) {
                  throw new Error('platform参数是必需的');
                }
                console.error(`🔍 搜索平台: ${platform}`);
                const response = await docSearchClient.searchDocs(platform);
                console.error(`✅ 搜索结果:`, response);
                result = {
                  content: [
                    {
                      type: 'text',
                      text: JSON.stringify(response, null, 2)
                    }
                  ]
                };
                break;
              }
              
              case 'get_document_content': {
                const { doc_path, keyword = '' } = args;
                if (!doc_path) {
                  throw new Error('doc_path参数是必需的');
                }
                const content = await docSearchClient.getDocContent(doc_path, { keyword });
                result = {
                  content: [
                    {
                      type: 'text',
                      text: JSON.stringify(content, null, 2)
                    }
                  ]
                };
                break;
              }
              
              case 'get_document_stats': {
                const stats = await docSearchClient.getDocumentStats();
                result = {
                  content: [
                    {
                      type: 'text',
                      text: JSON.stringify(stats, null, 2)
                    }
                  ]
                };
                break;
              }
              
              case 'get_available_platforms': {
                const platforms = ['android', 'ios', 'web', 'flutter', 'react-native', 'unity', 'electron', 'harmonyos', 'applet', 'server-side'];
                result = {
                  content: [
                    {
                      type: 'text',
                      text: JSON.stringify({ platforms }, null, 2)
                    }
                  ]
                };
                break;
              }
              
              default:
                throw new Error(`未知的工具: ${name}`);
            }
            
            const response = {
              jsonrpc: '2.0',
              id: request.id,
              result
            };
            stdout.write(JSON.stringify(response) + '\n');
            
          } catch (error) {
            console.error(`❌ 工具调用失败:`, error);
            const response = {
              jsonrpc: '2.0',
              id: request.id,
              error: {
                code: -32603,
                message: error instanceof Error ? error.message : String(error)
              }
            };
            stdout.write(JSON.stringify(response) + '\n');
          }
        }
      }
    } catch (error) {
      console.error('处理请求时出错:', error);
    }
  });
  
  stdin.on('end', () => {
    console.error('MCP客户端已关闭');
    process.exit(0);
  });
}

// 启动客户端
console.error('✅ 标准MCP客户端已启动');
handleMCPRequest().catch(console.error); 