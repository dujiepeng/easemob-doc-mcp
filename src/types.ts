// 文档搜索结果
export interface DocSearchResult {
  platform: string;
  results: string[];
  total: number;
  searchTime: number;
}

// 文档内容
export interface DocContent {
  docPath: string;
  content?: string;
  matches: DocMatch[];
  error?: string;
  contentLength?: number;
  matchesCount?: number;
}

// 文档匹配
export interface DocMatch {
  lineNumber: number;
  line: string;
  context: string;
  keyword?: string;
}

// SSE事件
export interface SSEEvent {
  type: 'start' | 'progress' | 'results_batch' | 'complete' | 'error' | 'end' | 'doc_info' | 'search_start' | 'match' | 'full_content';
  message?: string;
  data?: any;
  batch?: number;
  total_batches?: number;
  total_results?: number;
  docPath?: string;
  content_length?: number;
  matches_count?: number;
  keyword?: string;
  match_index?: number;
  total_matches?: number;
  content?: string;
}

// 客户端选项
export interface ClientOptions {
  baseUrl?: string;
  timeout?: number;
  headers?: Record<string, string>;
}

// 搜索选项
export interface SearchOptions {
  headers?: Record<string, string>;
}

// 文档内容选项
export interface DocContentOptions {
  keyword?: string;
  headers?: Record<string, string>;
}

// 健康检查
export interface HealthCheck {
  status: string;
  service: string;
  version?: string;
  timestamp?: string;
} 