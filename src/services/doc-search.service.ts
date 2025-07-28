import * as fs from 'fs-extra';
import * as path from 'path';
import { glob } from 'glob';
import { DocContent, DocMatch } from '../types';

export class DocSearchService {
  private docRoot: string;

  constructor() {
    // 文档根目录
    this.docRoot = path.join(process.cwd(), 'document');
    
    // 确保文档目录存在
    if (!fs.existsSync(this.docRoot)) {
      console.warn(`⚠️  文档目录不存在: ${this.docRoot}`);
      console.log('💡 请确保document目录存在于项目根目录中');
    }
  }

  /**
   * 搜索特定平台的文档目录
   */
  async searchPlatformDocs(platform: string): Promise<string[]> {
    try {
      // 确保平台名是小写的，以便统一比较
      const lowercasePlatform = platform.toLowerCase();
      
      // 获取所有可用的平台目录
      const dirs = await fs.readdir(this.docRoot);
      const platformDirs = dirs.filter(dir => {
        const fullPath = path.join(this.docRoot, dir);
        return fs.statSync(fullPath).isDirectory() && 
               dir.toLowerCase().includes(lowercasePlatform);
      });
      
      if (platformDirs.length === 0) {
        return [];
      }
      
      // 收集所有匹配平台的文档
      const results: string[] = [];
      
      for (const platformDir of platformDirs) {
        const platformPath = path.join(this.docRoot, platformDir);
        
        // 递归获取所有Markdown文件
        const pattern = path.join(platformPath, '**/*.md');
        const files = await glob(pattern, { windowsPathsNoEscape: true });
        
        for (const file of files) {
          // 转换为相对路径
          const relPath = path.relative(this.docRoot, file);
          results.push(relPath.replace(/\\/g, '/')); // 统一使用正斜杠
        }
      }
      
      return results;
    } catch (error) {
      console.error('搜索文档错误:', error);
      throw new Error(`搜索文档失败: ${error}`);
    }
  }

  /**
   * 获取文档内容，并根据关键字搜索相关内容
   */
  async getDocumentContent(docPath: string, keyword: string = ''): Promise<DocContent> {
    try {
      const fullPath = path.join(this.docRoot, docPath);
      
      // 检查文件是否存在
      if (!await fs.pathExists(fullPath)) {
        return {
          content: null,
          docPath,
          matches: [],
          error: '文档不存在'
        };
      }
      
      // 读取文件内容
      const content = await fs.readFile(fullPath, 'utf-8');
      
      // 如果没有关键字，返回全部内容
      if (!keyword || keyword.trim() === '') {
        return {
          content,
          docPath,
          matches: []
        };
      }
      
      // 搜索关键字
      const lines = content.split('\n');
      const matches: DocMatch[] = [];
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        if (line.toLowerCase().includes(keyword.toLowerCase())) {
          // 提取匹配行的上下文（前后各2行）
          const startLine = Math.max(0, i - 2);
          const endLine = Math.min(lines.length - 1, i + 2);
          
          const context = lines.slice(startLine, endLine + 1).join('\n');
          matches.push({
            lineNumber: i + 1,
            context,
            line
          });
        }
      }
      
      return {
        content,
        docPath,
        matches
      };
    } catch (error) {
      console.error('获取文档内容错误:', error);
      return {
        content: null,
        docPath,
        matches: [],
        error: `获取文档内容失败: ${error}`
      };
    }
  }

  /**
   * 获取所有可用的平台
   */
  async getAvailablePlatforms(): Promise<string[]> {
    try {
      const dirs = await fs.readdir(this.docRoot);
      const platformDirs = [];
      
      for (const dir of dirs) {
        const fullPath = path.join(this.docRoot, dir);
        const stat = await fs.stat(fullPath);
        if (stat.isDirectory()) {
          platformDirs.push(dir);
        }
      }
      
      return platformDirs;
    } catch (error) {
      console.error('获取平台列表错误:', error);
      return [];
    }
  }

  /**
   * 获取文档统计信息
   */
  async getDocumentStats(): Promise<{
    totalPlatforms: number;
    totalDocuments: number;
    platforms: Array<{
      name: string;
      documentCount: number;
    }>;
  }> {
    try {
      const platforms = await this.getAvailablePlatforms();
      const platformStats = [];
      let totalDocs = 0;
      
      for (const platform of platforms) {
        const docs = await this.searchPlatformDocs(platform);
        platformStats.push({
          name: platform,
          documentCount: docs.length
        });
        totalDocs += docs.length;
      }
      
      return {
        totalPlatforms: platforms.length,
        totalDocuments: totalDocs,
        platforms: platformStats
      };
    } catch (error) {
      console.error('获取文档统计错误:', error);
      return {
        totalPlatforms: 0,
        totalDocuments: 0,
        platforms: []
      };
    }
  }
} 