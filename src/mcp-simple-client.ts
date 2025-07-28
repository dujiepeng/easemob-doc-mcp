#!/usr/bin/env node

import EasemobDocSearchClient from './client';

// 从环境变量获取远程服务器URL
const remoteUrl = process.env.EASEMOB_API_URL || 'http://localhost:8000';
const docSearchClient = new EasemobDocSearchClient({
  baseUrl: remoteUrl
});

console.error(`🔗 连接到远程服务器: ${remoteUrl}`);

// 简单的 MCP 协议实现
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
        } else if (request.method === 'tools/call') {
          // 处理工具调用
          const { name, arguments: args } = request.params;
          
          try {
            let result;
            
            switch (name) {
              case 'search_platform_docs': {
                const { platform } = args;
                if (!platform) {
                  throw new Error('platform参数是必需的');
                }
                const results = await docSearchClient.searchDocs(platform);
                result = {
                  content: [
                    {
                      type: 'text',
                      text: JSON.stringify(results, null, 2)
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
console.error('✅ 简化MCP客户端已启动');
handleMCPRequest().catch(console.error); 