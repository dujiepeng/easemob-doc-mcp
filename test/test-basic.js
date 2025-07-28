const EasemobDocSearchClient = require('../dist/index.js');

async function testBasic() {
  console.log('🧪 开始基本功能测试...\n');

  const client = new EasemobDocSearchClient({
    baseUrl: 'http://localhost:8000'
  });

  try {
    // 测试健康检查
    console.log('1️⃣ 测试健康检查...');
    const health = await client.healthCheck();
    console.log('✅ 健康检查通过:', health.status);

    // 测试搜索文档
    console.log('\n2️⃣ 测试搜索文档...');
    const searchResult = await client.searchDocs('android');
    console.log(`✅ 搜索成功，找到 ${searchResult.results.length} 个文档`);

    // 测试获取文档内容
    if (searchResult.results.length > 0) {
      console.log('\n3️⃣ 测试获取文档内容...');
      const firstDoc = searchResult.results[0];
      const content = await client.getDocContent(firstDoc);
      console.log(`✅ 获取文档内容成功: ${content.docPath}`);
      console.log(`📄 内容长度: ${content.content?.length || 0} 字符`);
    }

    // 测试关键字搜索
    console.log('\n4️⃣ 测试关键字搜索...');
    const keywordResult = await client.getDocContent('android/overview.md', '初始化');
    console.log(`✅ 关键字搜索成功，找到 ${keywordResult.matches.length} 个匹配`);

    console.log('\n🎉 所有基本测试通过！');

  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    console.log('\n💡 请确保服务器正在运行:');
    console.log('   npm start');
  }
}

// 运行测试
testBasic(); 