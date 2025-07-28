# 使用 Node.js 18 Alpine 作为基础镜像（轻量级）
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 安装系统依赖（curl 用于健康检查）
RUN apk add --no-cache curl

# 复制 package 文件（利用 Docker 缓存层）
COPY package*.json ./

# 复制 scripts 目录（postinstall 脚本需要）
COPY scripts/ ./scripts/

# 安装所有依赖（包括开发依赖，用于构建）
RUN npm ci --only=production=false

# 复制源代码和配置文件
COPY src/ ./src/
COPY tsconfig.json ./

# 构建应用
RUN npm run build

# 删除开发依赖，只保留生产依赖
RUN npm prune --production

# 复制文档目录
COPY document/ ./document/

# 创建非 root 用户（安全最佳实践）
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# 更改文件所有权
RUN chown -R nodejs:nodejs /app

# 切换到非 root 用户
USER nodejs

# 暴露端口
EXPOSE 8000

# 健康检查（每30秒检查一次）
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["node", "dist/server.js"] 