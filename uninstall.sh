#!/bin/bash

# 环信文档搜索 MCP 服务卸载脚本
# 使用方法: bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/uninstall.sh)
# 指定端口: bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/uninstall.sh) --port 8080
# 指定传输协议: bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/uninstall.sh) --transport http --port 443 --host 0.0.0.0 --path /mcp/

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认配置
DEFAULT_TRANSPORT="http"
DEFAULT_HOST="0.0.0.0"
DEFAULT_PORT=443
DEFAULT_PATH="/mcp/"

TRANSPORT=$DEFAULT_TRANSPORT
HOST=$DEFAULT_HOST
PORT=$DEFAULT_PORT
PATH=$DEFAULT_PATH

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --transport|-t)
            TRANSPORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --port|-p)
            PORT="$2"
            shift 2
            ;;
        --path)
            PATH="$2"
            shift 2
            ;;
        --help|-h)
            echo "环信文档搜索 MCP 服务卸载脚本"
            echo ""
            echo "使用方法:"
            echo "  bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/uninstall.sh)"
            echo "  bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/uninstall.sh) --port 8080"
            echo "  bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/uninstall.sh) --transport http --port 443 --host 0.0.0.0 --path /mcp/"
            echo ""
            echo "参数:"
            echo "  --transport, -t TRANSPORT  传输协议 (stdio, http, sse) (默认: $DEFAULT_TRANSPORT)"
            echo "  --host HOST                HTTP传输时绑定的主机 (默认: $DEFAULT_HOST)"
            echo "  --port, -p PORT            HTTP传输时绑定的端口 (默认: $DEFAULT_PORT)"
            echo "  --path PATH                HTTP传输时绑定的路径 (默认: $DEFAULT_PATH)"
            echo "  --help, -h                 显示帮助信息"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            echo "使用 --help 查看帮助信息"
            exit 1
            ;;
    esac
done

# 验证传输协议
if [[ ! "$TRANSPORT" =~ ^(stdio|http|sse)$ ]]; then
    echo -e "${RED}[ERROR]${NC} 无效的传输协议: $TRANSPORT (必须是 stdio, http, 或 sse)"
    exit 1
fi

# 验证端口号（仅对http和sse传输）
if [[ "$TRANSPORT" =~ ^(http|sse)$ ]]; then
    if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
        echo -e "${RED}[ERROR]${NC} 无效的端口号: $PORT (必须是1-65535之间的数字)"
        exit 1
    fi
fi

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

print_info "传输协议: $TRANSPORT"
if [[ "$TRANSPORT" =~ ^(http|sse)$ ]]; then
    print_info "主机: $HOST"
    print_info "端口: $PORT"
    print_info "路径: $PATH"
fi

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

# 检查端口是否还在使用（仅对http和sse传输）
if [[ "$TRANSPORT" =~ ^(http|sse)$ ]]; then
    print_info "检查端口 $PORT 状态..."
    if netstat -tuln 2>/dev/null | grep -q ":$PORT "; then
        print_warning "端口 $PORT 仍被占用，可能需要手动检查"
    else
        print_success "端口 $PORT 已释放"
    fi
fi

print_success "=== 卸载完成 ==="
print_info "环信文档搜索 MCP 服务已完全移除" 