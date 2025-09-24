#!/bin/bash

# 环信文档更新脚本
# 从GitHub仓库拉取最新的文档文件

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCUMENT_DIR="$PROJECT_DIR/document"
UIKIT_DIR="$PROJECT_DIR/uikit"
CALLKIT_DIR="$PROJECT_DIR/callkit"
TEMP_DIR="$PROJECT_DIR/temp_docs"

# GitHub 仓库信息
GITHUB_REPO="https://github.com/easemob/easemob-doc.git"
GITHUB_BRANCH="doc-v2"

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 清理临时目录
cleanup() {
    if [ -d "$TEMP_DIR" ]; then
        print_info "清理临时目录..."
        rm -rf "$TEMP_DIR"
    fi
}

# 错误处理
handle_error() {
    print_error "更新文档过程中发生错误，请检查日志"
    cleanup
    exit 1
}

# 设置错误处理
trap handle_error ERR

# 主函数
main() {
    print_info "开始更新环信文档..."
    
    # 创建临时目录
    print_info "创建临时目录..."
    mkdir -p "$TEMP_DIR"
    
    # 克隆仓库
    print_info "克隆GitHub仓库 $GITHUB_REPO 分支 $GITHUB_BRANCH..."
    git clone --depth 1 --branch "$GITHUB_BRANCH" "$GITHUB_REPO" "$TEMP_DIR"
    
    # 确保目标目录存在
    mkdir -p "$DOCUMENT_DIR"
    mkdir -p "$UIKIT_DIR"
    mkdir -p "$CALLKIT_DIR"
    
    # 复制document目录
    if [ -d "$TEMP_DIR/docs/document" ]; then
        print_info "更新document目录..."
        rsync -a --delete "$TEMP_DIR/docs/document/" "$DOCUMENT_DIR/"
        print_success "document目录更新完成"
    else
        print_error "GitHub仓库中不存在docs/document目录"
    fi
    
    # 复制uikit目录
    if [ -d "$TEMP_DIR/docs/uikit" ]; then
        print_info "更新uikit目录..."
        rsync -a --delete "$TEMP_DIR/docs/uikit/" "$UIKIT_DIR/"
        print_success "uikit目录更新完成"
    else
        print_error "GitHub仓库中不存在docs/uikit目录"
    fi
    
    # 复制callkit目录
    if [ -d "$TEMP_DIR/docs/callkit" ]; then
        print_info "更新callkit目录..."
        rsync -a --delete "$TEMP_DIR/docs/callkit/" "$CALLKIT_DIR/"
        print_success "callkit目录更新完成"
    else
        print_error "GitHub仓库中不存在docs/callkit目录"
    fi
    
    # 清理临时目录
    cleanup
    
    print_success "文档更新完成！"
    print_info "document目录: $DOCUMENT_DIR"
    print_info "uikit目录: $UIKIT_DIR"
    print_info "callkit目录: $CALLKIT_DIR"
}

# 运行主函数
main
