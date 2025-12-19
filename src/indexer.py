import os
import shutil
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
import jieba
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.qparser import QueryParser
from whoosh.analysis import Tokenizer, Token, Analyzer
from whoosh.highlight import Highilighter, ContextFragmenter

# 自定义 Jieba 分词器适配 Whoosh
class JiebaTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False, keeporiginal=False, removestops=True,
                 start_pos=0, start_char=0, mode='', **kwargs):
        t = Token(positions, chars, removestops=removestops, mode=mode, **kwargs)
        seg_list = jieba.cut_for_search(value)  # 使用搜索引擎模式
        pos = start_pos
        for w in seg_list:
            t.original = t.text = w
            t.boost = 1.0
            if positions:
                t.pos = pos
            if chars:
                t.startchar = start_char
                t.endchar = start_char + len(w)
            yield t
            pos += 1
            start_char += len(w)

def JiebaAnalyzer():
    return JiebaTokenizer()

class DocIndexer:
    def __init__(self, index_dir: str = "indexdir"):
        self.index_dir = index_dir
        # 定义 Schema
        # path: 文档相对路径 (ID, 唯一)
        # content: 文档内容 (TEXT, 使用 Jieba 分词)
        # title: 标题 (TEXT, 使用 Jieba 分词)
        # platform: 平台 (ID, 存储)
        # doc_type: 文档类型 (ID, 存储)
        self.schema = Schema(
            path=ID(stored=True, unique=True),
            content=TEXT(stored=True, analyzer=JiebaAnalyzer()),
            title=TEXT(stored=True, analyzer=JiebaAnalyzer()),
            platform=ID(stored=True),
            doc_type=ID(stored=True)
        )
        self.ix = None

    def initialize_index(self, rebuild: bool = True):
        """初始化索引"""
        if rebuild and os.path.exists(self.index_dir):
            shutil.rmtree(self.index_dir)
            
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)
            self.ix = create_in(self.index_dir, self.schema)
        else:
            self.ix = open_dir(self.index_dir)

    def add_documents(self, documents: List[Dict[str, Any]]):
        """批量添加文档"""
        writer = self.ix.writer()
        for doc in documents:
            writer.add_document(
                path=doc['path'],
                content=doc['content'],
                title=doc.get('title', ''),
                platform=doc.get('platform', 'generic'),
                doc_type=doc.get('doc_type', 'unknown')
            )
        writer.commit()

    def search(self, query_str: str, limit: int = 10, doc_type: str = None, platform: str = None) -> List[Dict[str, Any]]:
        """执行搜索"""
        if not self.ix:
            return []

        results_data = []
        with self.ix.searcher() as searcher:
            # 构建查询
            # 默认在 content 和 title 中搜索
            parser = QueryParser("content", schema=self.ix.schema)
            # 允许搜索 title
            # query = parser.parse(query_str) 
            # 简单起见，我们主要搜 content，也可以用 MultifieldParser
            
            from whoosh.qparser import MultifieldParser
            parser = MultifieldParser(["title", "content"], schema=self.ix.schema)
            query = parser.parse(query_str)

            # 过滤逻辑 (Whoosh 过滤比较麻烦，这里先搜索后过滤，或者构造组合查询)
            # 为了简单和性能，如果指定了 platform/doc_type，应该作为 Filter 传入
            filter_query = None
            # 注意：Whoosh 的 filter 需要 Query 对象，这里简化处理，先只做文本搜索
            # 如果需要精确过滤，可以使用 Term 查询组合
            
            # 使用 searcher 搜索
            results = searcher.search(query, limit=limit if not (doc_type or platform) else limit * 5) # 稍微多取一点以便过滤

            # 设置高亮
            results.fragmenter = ContextFragmenter(maxchars=100, surround=30)

            for hit in results:
                # 后置过滤
                if doc_type and hit['doc_type'] != doc_type:
                    continue
                if platform and hit['platform'] != platform:
                    continue
                
                # 提取结果
                summary = hit.highlights("content")
                # 如果没有高亮（可能匹配的是 title），就截取前段
                if not summary:
                    summary = hit['content'][:200] + "..."

                results_data.append({
                    "path": hit['path'],
                    "score": hit.score,
                    "title": hit['title'],
                    "summary": summary,
                    "platform": hit['platform'],
                    "doc_type": hit['doc_type']
                })
                
                if len(results_data) >= limit:
                    break
                    
        return results_data

# 全局索引器实例
global_indexer = DocIndexer()

async def build_index_async(doc_root: Path, uikit_root: Path, callkit_root: Path):
    """异步构建索引"""
    print("开始构建全文索引...")
    
    # 在线程中运行 CPU 密集型任务
    await asyncio.to_thread(global_indexer.initialize_index, rebuild=True)
    
    documents = []
    
    def _read_and_collect(root: Path, doc_type: str):
        if not root.exists():
            return
            
        prefix_len = len(str(root)) + 1
        
        for walk_root, _, files in os.walk(root):
            for file in files:
                if file.endswith('.md'):
                    full_path = os.path.join(walk_root, file)
                    rel_path = full_path[prefix_len:]
                    
                    # 推断 Platform
                    # 规则: 路径的第一级目录通常是 platform
                    # 例如: android/quickstart.md -> platform=android
                    # uikit/chatuikit/android/xxx -> platform=android
                    
                    platform = "generic"
                    parts = rel_path.replace("\\", "/").split("/")
                    
                    if doc_type == "sdk":
                        if len(parts) > 0:
                            platform = parts[0]
                    elif doc_type in ["uikit", "callkit"]:
                        # uikit/chatuikit/android/... -> parts=["chatuikit", "android", ...]
                        # 我们尽量找像 platform 的部分
                        KNOWN_PLATFORMS = ["android", "ios", "web", "flutter", "react-native", "harmonyos", "windows", "linux", "unity", "electron", "applet"]
                        for p in parts:
                            if p.lower() in KNOWN_PLATFORMS:
                                platform = p.lower()
                                break
                    
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # 简单的标题提取:第一行 #
                        title = rel_path
                        lines = content.split('\n')
                        for line in lines:
                            if line.strip().startswith('# '):
                                title = line.strip()[2:].strip()
                                break
                                
                        documents.append({
                            "path": f"{doc_type}/{rel_path}",
                            "content": content,
                            "title": title,
                            "platform": platform,
                            "doc_type": doc_type
                        })
                    except Exception as e:
                        print(f"Skipping {full_path}: {e}")

    # 收集文档 (依然在线程中执行以避免阻塞)
    await asyncio.to_thread(_read_and_collect, doc_root, "sdk")
    await asyncio.to_thread(_read_and_collect, uikit_root, "uikit")
    await asyncio.to_thread(_read_and_collect, callkit_root, "callkit")
    
    print(f"扫描到 {len(documents)} 个文档，正在写入索引...")
    await asyncio.to_thread(global_indexer.add_documents, documents)
    print("全文索引构建完成!")
