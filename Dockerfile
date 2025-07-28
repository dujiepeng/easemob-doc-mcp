# 使用Node.js 18作为基础镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apk add --no-cache curl

# 复制package文件
COPY package*.json ./

# 复制scripts目录（postinstall脚本需要）
COPY scripts/ ./scripts/

# 安装所有依赖（包括开发依赖，用于构建）
RUN npm ci

# 复制源代码
COPY src/ ./src/
COPY tsconfig.json ./

# 构建应用
RUN npm run build

# 删除开发依赖，只保留生产依赖
RUN npm prune --production

# 复制文档
COPY document/ ./document/

# 创建非root用户
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# 更改文件所有权
RUN chown -R nodejs:nodejs /app
USER nodejs

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["node", "dist/server.js"] 