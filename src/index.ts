// 导出主要类
export { default as EasemobDocSearchClient } from './client';

// 导出类型定义
export type {
  DocSearchResult,
  DocContent,
  DocMatch,
  SSEEvent,
  ClientOptions,
  SearchOptions,
  DocContentOptions,
  HealthCheck
} from './types';

// 默认导出
export { default } from './client'; 