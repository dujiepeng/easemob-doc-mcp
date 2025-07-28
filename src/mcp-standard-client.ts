#!/usr/bin/env node

/**
 * 环信文档搜索 MCP 标准客户端
 * 
 * 这是一个自定义的 MCP (Model Context Protocol) 客户端实现，
 * 用于连接环信文档搜索服务。它实现了完整的 MCP 协议，
 * 包括 initialize、tools/list 和 tools/call 方法。
 * 
 * 主要功能：
 * - 连接到远程 HTTP API 服务器
 * - 提供文档搜索工具
 * - 支持流式响应
 */

import EasemobDocSearchClient from './client';

// 从环境变量获取远程服务器URL，默认为本地服务器
const remoteUrl = process.env.EASEMOB_API_URL || 'http://localhost:8000';
const docSearchClient = new EasemobDocSearchClient({
  baseUrl: remoteUrl
});

console.error(`🔗 连接到远程服务器: ${remoteUrl}`);

/**
 * 定义可用的 MCP 工具
 * 每个工具包含名称、描述和输入参数模式
 */
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

/**
 * 标准 MCP 协议实现
 * 处理来自 Cursor 或其他 MCP 客户端的请求
 */
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
        
        // 处理初始化请求
        if (request.method === 'initialize') {
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
        } 
        // 处理工具列表请求
        else if (request.method === 'tools/list') {
          const response = {
            jsonrpc: '2.0',
            id: request.id,
            result: {
              tools: tools
            }
          };
          stdout.write(JSON.stringify(response) + '\n');
        } 
        // 处理工具调用请求
        else if (request.method === 'tools/call') {
          const { name, arguments: args } = request.params;
          
          console.error(`🔧 调用工具: ${name}, 参数:`, args);
          
          try {
            let result;
            
            // 根据工具名称执行相应的操作
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
            
            // 返回成功响应
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