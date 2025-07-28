import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { DocSearchService } from './services/doc-search.service';

const app = express();
const port = process.env.PORT || 8000;

// 中间件
app.use(helmet());
app.use(compression());
app.use(cors());
app.use(express.json());

// 创建文档搜索服务实例
const docSearchService = new DocSearchService();

// 健康检查端点
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'easemob-doc-search',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// REST API 端点
app.get('/api/search-docs', async (req, res) => {
  try {
    const { platform } = req.query;
    
    if (!platform || typeof platform !== 'string') {
      return res.status(400).json({ error: 'platform参数是必需的' });
    }

    const results = await docSearchService.searchPlatformDocs(platform);
    res.json({ results });
  } catch (error) {
    console.error('搜索文档错误:', error);
    res.status(500).json({ error: '搜索文档失败' });
  }
});

app.get('/api/get-doc-content', async (req, res) => {
  try {
    const { path, keyword } = req.query;
    
    if (!path || typeof path !== 'string') {
      return res.status(400).json({ error: 'path参数是必需的' });
    }

    const keywordStr = typeof keyword === 'string' ? keyword : '';
    const result = await docSearchService.getDocumentContent(path, keywordStr);
    res.json(result);
  } catch (error) {
    console.error('获取文档内容错误:', error);
    res.status(500).json({ error: '获取文档内容失败' });
  }
});

// SSE 端点
app.get('/api/sse/search-docs', async (req, res) => {
  const { platform } = req.query;
  
  if (!platform || typeof platform !== 'string') {
    return res.status(400).json({ error: 'platform参数是必需的' });
  }

  // 设置SSE头部
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': '*'
  });

  try {
    // 发送开始事件
    res.write(`data: ${JSON.stringify({ type: 'start', message: `开始搜索 ${platform} 平台文档...` })}\n\n`);

    // 执行搜索
    const results = await docSearchService.searchPlatformDocs(platform);
    
    // 发送进度事件
    res.write(`data: ${JSON.stringify({ type: 'progress', message: `找到 ${results.length} 个文档` })}\n\n`);

    // 分批发送结果
    const batchSize = 10;
    for (let i = 0; i < results.length; i += batchSize) {
      const batch = results.slice(i, i + batchSize);
      const batchNum = Math.floor(i / batchSize) + 1;
      const totalBatches = Math.ceil(results.length / batchSize);
      
      res.write(`data: ${JSON.stringify({
        type: 'results_batch',
        data: batch,
        batch: batchNum,
        total_batches: totalBatches
      })}\n\n`);

      // 小延迟避免阻塞
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    // 发送完成事件
    res.write(`data: ${JSON.stringify({ type: 'complete', total_results: results.length })}\n\n`);
  } catch (error) {
    console.error('SSE搜索错误:', error);
    res.write(`data: ${JSON.stringify({ type: 'error', message: `搜索失败: ${error}` })}\n\n`);
  } finally {
    res.end();
  }
});

app.get('/api/sse/get-doc-content', async (req, res) => {
  const { path, keyword } = req.query;
  
  if (!path || typeof path !== 'string') {
    return res.status(400).json({ error: 'path参数是必需的' });
  }

  const keywordStr = typeof keyword === 'string' ? keyword : '';

  // 设置SSE头部
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': '*'
  });

  try {
    // 发送开始事件
    res.write(`data: ${JSON.stringify({ type: 'start', message: `开始获取文档: ${path}` })}\n\n`);

    // 获取文档内容
    const result = await docSearchService.getDocumentContent(path, keywordStr);
    
    if (result.error) {
      res.write(`data: ${JSON.stringify({ type: 'error', message: result.error })}\n\n`);
      return res.end();
    }

    // 发送文档信息
    res.write(`data: ${JSON.stringify({
      type: 'doc_info',
      docPath: result.docPath,
      content_length: result.content?.length || 0,
      matches_count: result.matches.length
    })}\n\n`);

    // 如果有搜索关键字，发送匹配结果
    if (keywordStr && result.matches.length > 0) {
      res.write(`data: ${JSON.stringify({ type: 'search_start', keyword: keywordStr })}\n\n`);
      
      for (let i = 0; i < result.matches.length; i++) {
        const match = result.matches[i];
        res.write(`data: ${JSON.stringify({
          type: 'match',
          match_index: i + 1,
          total_matches: result.matches.length,
          data: match
        })}\n\n`);
        
        // 小延迟
        await new Promise(resolve => setTimeout(resolve, 50));
      }
    }

    // 发送完整内容（如果内容不太大）
    if (result.content && result.content.length < 50000) {
      res.write(`data: ${JSON.stringify({
        type: 'full_content',
        content: result.content
      })}\n\n`);
    }

    // 发送完成事件
    res.write(`data: ${JSON.stringify({ type: 'complete', message: '文档内容获取完成' })}\n\n`);
  } catch (error) {
    console.error('SSE获取文档内容错误:', error);
    res.write(`data: ${JSON.stringify({ type: 'error', message: `获取文档内容失败: ${error}` })}\n\n`);
  } finally {
    res.end();
  }
});

// 错误处理中间件
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('服务器错误:', err);
  res.status(500).json({ error: '服务器内部错误' });
});

// 404处理
app.use('*', (req, res) => {
  res.status(404).json({ error: '接口不存在' });
});

// 启动服务器
app.listen(port, () => {
  console.log(`🚀 环信文档搜索服务器启动成功！`);
  console.log(`📍 地址: http://localhost:${port}`);
  console.log(`📡 API文档: http://localhost:${port}/api`);
  console.log(`🔍 健康检查: http://localhost:${port}/health`);
  console.log(`\n📋 可用端点:`);
  console.log(`  - GET /health - 健康检查`);
  console.log(`  - GET /api/search-docs?platform={platform} - 搜索文档`);
  console.log(`  - GET /api/get-doc-content?path={path}&keyword={keyword} - 获取文档内容`);
  console.log(`  - GET /api/sse/search-docs?platform={platform} - SSE流式搜索`);
  console.log(`  - GET /api/sse/get-doc-content?path={path}&keyword={keyword} - SSE流式获取内容`);
});

export default app; 