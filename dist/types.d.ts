export interface DocSearchResult {
    platform: string;
    results: string[];
    total: number;
    searchTime: number;
}
export interface DocContent {
    docPath: string;
    content?: string;
    matches: DocMatch[];
    error?: string;
    contentLength?: number;
    matchesCount?: number;
}
export interface DocMatch {
    lineNumber: number;
    line: string;
    context: string;
    keyword?: string;
}
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
export interface ClientOptions {
    baseUrl?: string;
    timeout?: number;
    headers?: Record<string, string>;
}
export interface SearchOptions {
    headers?: Record<string, string>;
}
export interface DocContentOptions {
    keyword?: string;
    headers?: Record<string, string>;
}
export interface HealthCheck {
    status: string;
    service: string;
    version?: string;
    timestamp?: string;
}
//# sourceMappingURL=types.d.ts.map