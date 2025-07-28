#!/bin/bash

# 环信文档搜索服务快速启动脚本

set -e

echo "🚀 环信文档搜索服务快速启动"
echo "================================"

# 检查Node.js环境
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装Node.js 16+"
    exit 1
fi

# 检查npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装，请先安装npm"
    exit 1
fi

# 检查Node.js版本
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js版本过低，需要16+版本"
    exit 1
fi

echo "✅ 检测到Node.js环境 (版本: $(node -v))"

# 安装依赖
echo "📦 安装依赖..."
npm install

# 构建项目
echo "🔨 构建TypeScript..."
npm run build

# 启动服务器
echo "🚀 启动服务器..."
npm start 