import fetch, { Response } from 'node-fetch';
import { 
  DocSearchResult, 
  DocContent, 
  SSEEvent, 
  ClientOptions, 
  SearchOptions, 
  DocContentOptions,
  HealthCheck 
} from './types';

export class EasemobDocSearchClient {
  private baseUrl: string;
  private timeout: number;
  private headers: Record<string, string>;

  constructor(options: ClientOptions = {}) {
    this.baseUrl = options.baseUrl || 'http://localhost:8000';
    this.timeout = options.timeout || 30000;
    this.headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };
  }

  /**
   * 健康检查
   */
  async healthCheck(): Promise<HealthCheck> {
    const response = await this.request('/health');
    return response as HealthCheck;
  }

  /**
   * 搜索平台文档（REST API）
   */
  async searchDocs(platform: string): Promise<DocSearchResult> {
    const response = await this.request(`/api/search-docs?platform=${encodeURIComponent(platform)}`);
    return response as DocSearchResult;
  }

  /**
   * 获取文档内容（REST API）
   */
  async getDocContent(path: string, keyword?: string): Promise<DocContent> {
    const params = new URLSearchParams();
    params.append('path', path);
    if (keyword) {
      params.append('keyword', keyword);
    }
    
    const response = await this.request(`/api/get-doc-content?${params.toString()}`);
    return response as DocContent;
  }

  /**
   * 流式搜索文档（SSE）
   */
  async *searchDocsStream(platform: string): AsyncGenerator<SSEEvent, void, unknown> {
    const url = `${this.baseUrl}/api/sse/search-docs?platform=${encodeURIComponent(platform)}`;
    
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'text/event-stream',
          'Cache-Control': 'no-cache',
          ...this.headers
        },
        timeout: this.timeout
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      if (!response.body) {
        throw new Error('No response body');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      try {
        while (true) {
          const { done, value } = await reader.read();
          
          if (done) {
            break;
          }

          const chunk = decoder.decode(value, { stream: true });
          const events = this.parseSSEChunk(chunk);
          
          for (const event of events) {
            if (event) {
              yield event;
            }
          }
        }
      } finally {
        reader.releaseLock();
      }
    } catch (error) {
      yield {
        type: 'error',
        message: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * 流式获取文档内容（SSE）
   */
  async *getDocContentStream(path: string, keyword?: string): AsyncGenerator<SSEEvent, void, unknown> {
    const params = new URLSearchParams();
    params.append('path', path);
    if (keyword) {
      params.append('keyword', keyword);
    }
    
    const url = `${this.baseUrl}/api/sse/get-doc-content?${params.toString()}`;
    
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'text/event-stream',
          'Cache-Control': 'no-cache',
          ...this.headers
        },
        timeout: this.timeout
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      if (!response.body) {
        throw new Error('No response body');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      try {
        while (true) {
          const { done, value } = await reader.read();
          
          if (done) {
            break;
          }

          const chunk = decoder.decode(value, { stream: true });
          const events = this.parseSSEChunk(chunk);
          
          for (const event of events) {
            if (event) {
              yield event;
            }
          }
        }
      } finally {
        reader.releaseLock();
      }
    } catch (error) {
      yield {
        type: 'error',
        message: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * 智能搜索 - 根据选项选择REST或SSE
   */
  async searchDocsSmart(options: SearchOptions): Promise<DocSearchResult | AsyncGenerator<SSEEvent, void, unknown>> {
    if (options.useSSE) {
      return this.searchDocsStream(options.platform);
    } else {
      return this.searchDocs(options.platform);
    }
  }

  /**
   * 智能获取文档内容 - 根据选项选择REST或SSE
   */
  async getDocContentSmart(options: DocContentOptions): Promise<DocContent | AsyncGenerator<SSEEvent, void, unknown>> {
    if (options.useSSE) {
      return this.getDocContentStream(options.path, options.keyword);
    } else {
      return this.getDocContent(options.path, options.keyword);
    }
  }

  /**
   * 通用请求方法
   */
  private async request(endpoint: string): Promise<any> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: this.headers,
      timeout: this.timeout
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * 解析SSE数据块
   */
  private parseSSEChunk(chunk: string): SSEEvent[] {
    const events: SSEEvent[] = [];
    const lines = chunk.split('\n');
    
    let currentData = '';
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6); // 移除 'data: ' 前缀
        
        if (data.trim() === '') {
          continue;
        }
        
        try {
          const event = JSON.parse(data);
          events.push(event);
        } catch (error) {
          console.warn('Failed to parse SSE data:', data);
        }
      }
    }
    
    return events;
  }
}

// 默认导出
export default EasemobDocSearchClient; 