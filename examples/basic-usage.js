const EasemobDocSearchClient = require('../dist/index.js');

async function basicExample() {
  // 创建客户端实例
  const client = new EasemobDocSearchClient({
    baseUrl: 'http://localhost:8000'
  });

  try {
    // 健康检查
    console.log('🔍 检查服务状态...');
    const health = await client.healthCheck();
    console.log('✅ 服务状态:', health.status);

    // 搜索Android平台文档
    console.log('\n📱 搜索Android平台文档...');
    const searchResult = await client.searchDocs('android');
    console.log(`✅ 找到 ${searchResult.results.length} 个文档`);

    // 获取第一个文档的内容
    if (searchResult.results.length > 0) {
      const firstDoc = searchResult.results[0];
      console.log(`\n📖 获取文档内容: ${firstDoc}`);
      
      const docContent = await client.getDocContent(firstDoc);
      console.log(`📄 文档长度: ${docContent.content?.length || 0} 字符`);
      console.log(`🔍 匹配数量: ${docContent.matches.length}`);
    }

  } catch (error) {
    console.error('❌ 错误:', error.message);
  }
}

// 运行示例
basicExample(); 