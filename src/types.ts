// 文档搜索结果类型
export interface DocSearchResult {
  results: string[];
}

// 文档内容类型
export interface DocContent {
  content: string | null;
  docPath: string;
  matches: DocMatch[];
  error?: string;
}

// 文档匹配项类型
export interface DocMatch {
  lineNumber: number;
  context: string;
  line: string;
}

// SSE事件类型
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

// 客户端配置选项
export interface ClientOptions {
  baseUrl?: string;
  timeout?: number;
  headers?: Record<string, string>;
}

// 搜索选项
export interface SearchOptions {
  platform: string;
  useSSE?: boolean;
}

// 文档内容获取选项
export interface DocContentOptions {
  path: string;
  keyword?: string;
  useSSE?: boolean;
}

// 健康检查响应
export interface HealthCheck {
  status: string;
  service: string;
} 