const EasemobDocSearchClient = require('../dist/index.js');

async function sseExample() {
  // 创建客户端实例
  const client = new EasemobDocSearchClient({
    baseUrl: 'http://localhost:8000'
  });

  try {
    console.log('🔍 开始SSE流式搜索Android平台文档...\n');

    // 使用SSE流式搜索
    const stream = client.searchDocsStream('android');
    
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
          event.data?.forEach(doc => {
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

    console.log('\n📖 开始SSE流式获取文档内容...\n');

    // 使用SSE流式获取文档内容
    const contentStream = client.getDocContentStream('android/overview.md', '初始化');
    
    for await (const event of contentStream) {
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
          break;
        case 'complete':
          console.log(`\n✅ ${event.message}`);
          break;
        case 'error':
          console.error(`❌ 错误: ${event.message}`);
          break;
      }
    }

  } catch (error) {
    console.error('❌ 错误:', error.message);
  }
}

// 运行示例
sseExample(); 