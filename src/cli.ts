#!/usr/bin/env node

import { Command } from 'commander';
import EasemobDocSearchClient from './client';
import { SSEEvent } from './types';

const program = new Command();

program
  .name('easemob-doc-search')
  .description('环信文档搜索服务命令行工具')
  .version('1.0.0');

// 全局选项
program
  .option('-u, --url <url>', '服务器URL', 'http://localhost:8000')
  .option('-t, --timeout <timeout>', '请求超时时间(毫秒)', '30000');

// 健康检查命令
program
  .command('health')
  .description('检查服务健康状态')
  .action(async (options: any) => {
    try {
      const client = new EasemobDocSearchClient({
        baseUrl: options.parent.url,
        timeout: parseInt(options.parent.timeout)
      });
      
      const health = await client.healthCheck();
      console.log('✅ 服务状态:', health.status);
      console.log('🔧 服务名称:', health.service);
    } catch (error) {
      console.error('❌ 健康检查失败:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// 搜索文档命令
program
  .command('search')
  .description('搜索平台文档')
  .argument('<platform>', '平台名称 (如: android, ios, web)')
  .option('-s, --stream', '使用SSE流式响应')
  .action(async (platform: string, options: any) => {
    try {
      const client = new EasemobDocSearchClient({
        baseUrl: options.parent.url,
        timeout: parseInt(options.parent.timeout)
      });

      if (options.stream) {
        console.log(`🔍 开始流式搜索 ${platform} 平台文档...\n`);
        
        const stream = client.searchDocsStream(platform);
        for await (const event of stream) {
          switch (event.type) {
            case 'start':
              console.log(`📡 ${event.message}`);
              break;
            case 'progress':
              console.log(`📊 ${event.message}`);
              break;
            case 'results_batch':
              console.log(`📄 批次 ${event.batch}/${event.total_batches}:`);
              event.data?.forEach((doc: string) => {
                console.log(`   - ${doc}`);
              });
              break;
            case 'complete':
              console.log(`✅ 搜索完成，共找到 ${event.total_results} 个文档`);
              break;
            case 'error':
              console.error(`❌ 错误: ${event.message}`);
              break;
          }
        }
      } else {
        console.log(`🔍 搜索 ${platform} 平台文档...`);
        const result = await client.searchDocs(platform);
        console.log(`✅ 找到 ${result.results.length} 个文档:\n`);
        result.results.forEach(doc => {
          console.log(`📄 ${doc}`);
        });
      }
    } catch (error) {
      console.error('❌ 搜索失败:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// 获取文档内容命令
program
  .command('content')
  .description('获取文档内容')
  .argument('<path>', '文档路径')
  .option('-k, --keyword <keyword>', '搜索关键字')
  .option('-s, --stream', '使用SSE流式响应')
  .action(async (path: string, options: any) => {
    try {
      const client = new EasemobDocSearchClient({
        baseUrl: options.parent.url,
        timeout: parseInt(options.parent.timeout)
      });

      if (options.stream) {
        console.log(`📖 开始流式获取文档: ${path}\n`);
        
        const stream = client.getDocContentStream(path, options.keyword);
        for await (const event of stream) {
          switch (event.type) {
            case 'start':
              console.log(`📡 ${event.message}`);
              break;
            case 'doc_info':
              console.log(`📄 文档信息:`);
              console.log(`   路径: ${event.docPath}`);
              console.log(`   内容长度: ${event.content_length} 字符`);
              console.log(`   匹配数量: ${event.matches_count}`);
              break;
            case 'search_start':
              console.log(`🔍 开始搜索关键字: "${event.keyword}"`);
              break;
            case 'match':
              console.log(`\n📍 匹配 ${event.match_index}/${event.total_matches}:`);
              console.log(`   行号: ${event.data.lineNumber}`);
              console.log(`   内容: ${event.data.line}`);
              console.log(`   上下文:\n${event.data.context}`);
              break;
            case 'full_content':
              console.log(`\n📄 完整文档内容:`);
              console.log(event.content);
              break;
            case 'complete':
              console.log(`\n✅ ${event.message}`);
              break;
            case 'error':
              console.error(`❌ 错误: ${event.message}`);
              break;
          }
        }
      } else {
        console.log(`📖 获取文档内容: ${path}`);
        if (options.keyword) {
          console.log(`🔍 搜索关键字: ${options.keyword}`);
        }
        
        const result = await client.getDocContent(path, options.keyword);
        
        if (result.error) {
          console.error(`❌ 错误: ${result.error}`);
          process.exit(1);
        }
        
        console.log(`\n📄 文档路径: ${result.docPath}`);
        console.log(`📊 内容长度: ${result.content?.length || 0} 字符`);
        console.log(`🔍 匹配数量: ${result.matches.length}`);
        
        if (result.matches.length > 0) {
          console.log(`\n📍 匹配结果:`);
          result.matches.forEach((match, index) => {
            console.log(`\n${index + 1}. 行号: ${match.lineNumber}`);
            console.log(`   内容: ${match.line}`);
            console.log(`   上下文:\n${match.context}`);
          });
        }
        
        if (result.content && result.content.length < 1000) {
          console.log(`\n📄 完整内容:\n${result.content}`);
        }
      }
    } catch (error) {
      console.error('❌ 获取文档内容失败:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// 启动服务器命令
program
  .command('serve')
  .description('启动文档搜索服务器')
  .option('-p, --port <port>', '服务器端口', '8000')
  .option('-m, --mode <mode>', '运行模式 (api|mcp|both)', 'api')
  .action(async (options: any) => {
    console.log('🚀 启动环信文档搜索服务器...');
    console.log(`📍 端口: ${options.port}`);
    console.log(`🔧 模式: ${options.mode}`);
    console.log('\n💡 提示: 请确保Python环境和依赖已安装');
    console.log('📦 依赖: pip install -r requirements.txt');
    console.log('\n🔄 正在启动服务器...\n');
    
    // 这里可以启动Python服务器进程
    const { spawn } = require('child_process');
    const pythonProcess = spawn('python', [
      'fastmcp_server/main.py',
      '--mode', options.mode
    ], {
      stdio: 'inherit'
    });
    
    pythonProcess.on('error', (error: Error) => {
      console.error('❌ 启动服务器失败:', error.message);
      console.log('💡 请确保Python环境和依赖已正确安装');
      process.exit(1);
    });
    
    pythonProcess.on('exit', (code: number) => {
      if (code !== 0) {
        console.error(`❌ 服务器异常退出，退出码: ${code}`);
        process.exit(code);
      }
    });
  });

// 解析命令行参数
program.parse(); 