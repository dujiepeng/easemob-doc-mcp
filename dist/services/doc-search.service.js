"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.DocSearchService = void 0;
const fs = __importStar(require("fs-extra"));
const path = __importStar(require("path"));
const glob_1 = require("glob");
class DocSearchService {
    constructor() {
        this.docRoot = path.join(process.cwd(), 'document');
    }
    /**
     * 搜索平台文档
     */
    async searchPlatformDocs(platform) {
        try {
            const platformPath = path.join(this.docRoot, platform);
            // 检查平台目录是否存在
            if (!await fs.pathExists(platformPath)) {
                return [];
            }
            // 搜索所有.md文件
            const pattern = path.join(platformPath, '**/*.md');
            const files = await (0, glob_1.glob)(pattern, { nodir: true });
            // 返回相对路径
            return files.map(file => {
                const relativePath = path.relative(this.docRoot, file);
                return relativePath.replace(/\\/g, '/'); // 统一使用正斜杠
            });
        }
        catch (error) {
            console.error('搜索平台文档失败:', error);
            return [];
        }
    }
    /**
     * 获取文档内容
     */
    async getDocumentContent(docPath, keyword = '') {
        try {
            const fullPath = path.join(this.docRoot, docPath);
            // 检查文件是否存在
            if (!await fs.pathExists(fullPath)) {
                return {
                    docPath,
                    content: undefined,
                    matches: [],
                    error: '文件不存在'
                };
            }
            // 读取文件内容
            const content = await fs.readFile(fullPath, 'utf-8');
            // 如果没有关键字，直接返回内容
            if (!keyword.trim()) {
                return {
                    docPath,
                    content,
                    matches: [],
                    contentLength: content.length,
                    matchesCount: 0
                };
            }
            // 搜索关键字
            const matches = [];
            const lines = content.split('\n');
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                if (line.toLowerCase().includes(keyword.toLowerCase())) {
                    // 获取上下文（前后各2行）
                    const start = Math.max(0, i - 2);
                    const end = Math.min(lines.length, i + 3);
                    const context = lines.slice(start, end).join('\n');
                    matches.push({
                        lineNumber: i + 1,
                        line: line.trim(),
                        context: context.trim(),
                        keyword
                    });
                }
            }
            return {
                docPath,
                content: undefined, // 有匹配时返回undefined，避免内容过大
                matches,
                contentLength: content.length,
                matchesCount: matches.length
            };
        }
        catch (error) {
            console.error('获取文档内容失败:', error);
            return {
                docPath,
                content: undefined,
                matches: [],
                error: error instanceof Error ? error.message : '未知错误'
            };
        }
    }
    /**
     * 获取可用平台列表
     */
    async getAvailablePlatforms() {
        try {
            const items = await fs.readdir(this.docRoot);
            const platforms = [];
            for (const item of items) {
                const itemPath = path.join(this.docRoot, item);
                const stat = await fs.stat(itemPath);
                if (stat.isDirectory()) {
                    platforms.push(item);
                }
            }
            return platforms.sort();
        }
        catch (error) {
            console.error('获取平台列表失败:', error);
            return [];
        }
    }
    /**
     * 获取文档统计信息
     */
    async getDocumentStats() {
        try {
            const platforms = await this.getAvailablePlatforms();
            const stats = {};
            let totalFiles = 0;
            for (const platform of platforms) {
                const platformPath = path.join(this.docRoot, platform);
                const pattern = path.join(platformPath, '**/*.md');
                const files = await (0, glob_1.glob)(pattern, { nodir: true });
                stats[platform] = files.length;
                totalFiles += files.length;
            }
            return {
                totalFiles,
                totalPlatforms: platforms.length,
                platforms: stats
            };
        }
        catch (error) {
            console.error('获取文档统计失败:', error);
            return {
                totalFiles: 0,
                totalPlatforms: 0,
                platforms: {}
            };
        }
    }
}
exports.DocSearchService = DocSearchService;
//# sourceMappingURL=doc-search.service.js.map