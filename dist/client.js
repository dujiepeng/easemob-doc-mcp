"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.EasemobDocSearchClient = void 0;
const node_fetch_1 = __importDefault(require("node-fetch"));
class EasemobDocSearchClient {
    constructor(options = {}) {
        this.baseUrl = options.baseUrl || 'http://localhost:8000';
        this.timeout = options.timeout || 30000;
    }
    /**
     * 搜索平台文档
     */
    async searchDocs(platform, options = {}) {
        const url = new URL('/api/search-docs', this.baseUrl);
        url.searchParams.set('platform', platform);
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        try {
            const response = await (0, node_fetch_1.default)(url.toString(), {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        }
        catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }
    /**
     * 流式搜索平台文档
     */
    async *searchDocsStream(platform) {
        const url = new URL('/api/sse/search-docs', this.baseUrl);
        url.searchParams.set('platform', platform);
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        try {
            const response = await (0, node_fetch_1.default)(url.toString(), {
                method: 'GET',
                headers: {
                    'Accept': 'text/event-stream',
                    'Cache-Control': 'no-cache'
                },
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            if (!response.body) {
                throw new Error('Response body is null');
            }
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            try {
                while (true) {
                    const { done, value } = await reader.read();
                    if (done)
                        break;
                    const chunk = decoder.decode(value, { stream: true });
                    const lines = chunk.split('\n');
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const data = line.slice(6);
                            if (data === '[DONE]') {
                                return;
                            }
                            try {
                                const event = JSON.parse(data);
                                yield event;
                            }
                            catch (e) {
                                console.warn('Failed to parse SSE event:', data);
                            }
                        }
                    }
                }
            }
            finally {
                reader.releaseLock();
            }
        }
        catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }
    /**
     * 获取文档内容
     */
    async getDocContent(docPath, options = {}) {
        const url = new URL('/api/get-doc-content', this.baseUrl);
        url.searchParams.set('path', docPath);
        if (options.keyword) {
            url.searchParams.set('keyword', options.keyword);
        }
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        try {
            const response = await (0, node_fetch_1.default)(url.toString(), {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        }
        catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }
    /**
     * 流式获取文档内容
     */
    async *getDocContentStream(docPath, keyword) {
        const url = new URL('/api/sse/get-doc-content', this.baseUrl);
        url.searchParams.set('path', docPath);
        if (keyword) {
            url.searchParams.set('keyword', keyword);
        }
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        try {
            const response = await (0, node_fetch_1.default)(url.toString(), {
                method: 'GET',
                headers: {
                    'Accept': 'text/event-stream',
                    'Cache-Control': 'no-cache'
                },
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            if (!response.body) {
                throw new Error('Response body is null');
            }
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            try {
                while (true) {
                    const { done, value } = await reader.read();
                    if (done)
                        break;
                    const chunk = decoder.decode(value, { stream: true });
                    const lines = chunk.split('\n');
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const data = line.slice(6);
                            if (data === '[DONE]') {
                                return;
                            }
                            try {
                                const event = JSON.parse(data);
                                yield event;
                            }
                            catch (e) {
                                console.warn('Failed to parse SSE event:', data);
                            }
                        }
                    }
                }
            }
            finally {
                reader.releaseLock();
            }
        }
        catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }
    /**
     * 健康检查
     */
    async healthCheck() {
        const url = new URL('/health', this.baseUrl);
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        try {
            const response = await (0, node_fetch_1.default)(url.toString(), {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        }
        catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }
    /**
     * 获取文档统计信息
     */
    async getDocumentStats() {
        const url = new URL('/api/stats', this.baseUrl);
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        try {
            const response = await (0, node_fetch_1.default)(url.toString(), {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        }
        catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }
}
exports.EasemobDocSearchClient = EasemobDocSearchClient;
exports.default = EasemobDocSearchClient;
//# sourceMappingURL=client.js.map