import { DocContent } from '../types';
export declare class DocSearchService {
    private docRoot;
    constructor();
    /**
     * 搜索平台文档
     */
    searchPlatformDocs(platform: string): Promise<string[]>;
    /**
     * 获取文档内容
     */
    getDocumentContent(docPath: string, keyword?: string): Promise<DocContent>;
    /**
     * 获取可用平台列表
     */
    getAvailablePlatforms(): Promise<string[]>;
    /**
     * 获取文档统计信息
     */
    getDocumentStats(): Promise<{
        totalFiles: number;
        totalPlatforms: number;
        platforms: Record<string, number>;
    }>;
}
//# sourceMappingURL=doc-search.service.d.ts.map