const EasemobDocSearchClient = require('../dist/index.js');

async function testSSE() {
  console.log('🧪 开始测试SSE功能...\n');

  const client = new EasemobDocSearchClient({
    baseUrl: 'http://localhost:8000'
  });

  try {
    // 测试健康检查
    console.log('1️⃣ 测试健康检查...');
    const health = await client.healthCheck();
    console.log('✅ 健康检查通过:', health.status);

    // 测试SSE搜索
    console.log('\n2️⃣ 测试SSE搜索文档...');
    const searchStream = client.searchDocsStream('android');
    let searchCount = 0;
    
    for await (const event of searchStream) {
      switch (event.type) {
        case 'start':
          console.log(`📡 ${event.message}`);
          break;
        case 'progress':
          console.log(`📊 ${event.message}`);
          break;
        case 'results_batch':
          searchCount += event.data?.length || 0;
          console.log(`📄 批次 ${event.batch}/${event.total_batches}: ${event.data?.length || 0} 个文档`);
          break;
        case 'complete':
          console.log(`✅ 搜索完成，共找到 ${event.total_results} 个文档`);
          break;
        case 'error':
          console.error(`❌ 搜索错误: ${event.message}`);
          return;
      }
    }

    // 测试SSE获取文档内容
    console.log('\n3️⃣ 测试SSE获取文档内容...');
    const contentStream = client.getDocContentStream('android/overview.md', '初始化');
    let matchCount = 0;
    
    for await (const event of contentStream) {
      switch (event.type) {
        case 'start':
          console.log(`📡 ${event.message}`);
          break;
        case 'doc_info':
          console.log(`📄 文档信息: ${event.docPath}, 长度: ${event.content_length} 字符`);
          break;
        case 'search_start':
          console.log(`🔍 开始搜索关键字: "${event.keyword}"`);
          break;
        case 'match':
          matchCount++;
          console.log(`📍 匹配 ${event.match_index}/${event.total_matches}: 行${event.data.lineNumber}`);
          break;
        case 'complete':
          console.log(`✅ 内容获取完成，找到 ${matchCount} 个匹配`);
          break;
        case 'error':
          console.error(`❌ 内容获取错误: ${event.message}`);
          return;
      }
    }

    console.log('\n🎉 所有SSE测试通过！');

  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    console.log('\n💡 请确保服务器正在运行:');
    console.log('   cd fastmcp_server && python main.py --mode api');
  }
}

// 运行测试
testSSE(); 