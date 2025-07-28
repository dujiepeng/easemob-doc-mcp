import { DocSearchResult, DocContent, SSEEvent, ClientOptions, SearchOptions, DocContentOptions, HealthCheck } from './types';
export declare class EasemobDocSearchClient {
    private baseUrl;
    private timeout;
    constructor(options?: ClientOptions);
    /**
     * 搜索平台文档
     */
    searchDocs(platform: string, options?: SearchOptions): Promise<DocSearchResult>;
    /**
     * 流式搜索平台文档
     */
    searchDocsStream(platform: string): AsyncGenerator<SSEEvent, void, unknown>;
    /**
     * 获取文档内容
     */
    getDocContent(docPath: string, options?: DocContentOptions): Promise<DocContent>;
    /**
     * 流式获取文档内容
     */
    getDocContentStream(docPath: string, keyword?: string): AsyncGenerator<SSEEvent, void, unknown>;
    /**
     * 健康检查
     */
    healthCheck(): Promise<HealthCheck>;
    /**
     * 获取文档统计信息
     */
    getDocumentStats(): Promise<any>;
}
export default EasemobDocSearchClient;
//# sourceMappingURL=client.d.ts.map