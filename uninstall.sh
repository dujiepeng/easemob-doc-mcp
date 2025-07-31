#!/bin/bash

# 环信文档搜索 MCP 服务卸载脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 配置变量
PROJECT_NAME="easemob-doc-mcp"
PROJECT_DIR="/opt/$PROJECT_NAME"

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

echo -e "${RED}"
echo "=========================================="
echo "  环信文档搜索 MCP 服务卸载脚本"
echo "=========================================="
echo -e "${NC}"

print_warning "此操作将完全移除环信文档搜索 MCP 服务"
read -p "是否继续？(y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "取消卸载"
    exit 0
fi

# 停止并禁用服务
print_info "停止服务..."
if sudo systemctl is-active --quiet easemob-doc-mcp; then
    sudo systemctl stop easemob-doc-mcp
    print_success "服务已停止"
else
    print_info "服务未运行"
fi

# 禁用服务
print_info "禁用服务..."
sudo systemctl disable easemob-doc-mcp 2>/dev/null || true

# 删除服务文件
print_info "删除服务文件..."
sudo rm -f /etc/systemd/system/easemob-doc-mcp.service
sudo systemctl daemon-reload

# 删除项目目录
print_info "删除项目目录..."
if [[ -d "$PROJECT_DIR" ]]; then
    sudo rm -rf $PROJECT_DIR
    print_success "项目目录已删除"
else
    print_info "项目目录不存在"
fi

# 清理日志
print_info "清理日志..."
sudo journalctl --vacuum-time=1s --unit=easemob-doc-mcp 2>/dev/null || true

print_success "=== 卸载完成 ==="
print_info "环信文档搜索 MCP 服务已完全移除" 