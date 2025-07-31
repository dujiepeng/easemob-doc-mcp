#!/bin/bash

# 环信文档搜索 MCP 服务一键部署脚本
# 使用方法: bash <(curl -s -L https://raw.githubusercontent.com/dujiepeng/easemob-doc-mcp/main/install.sh)

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置变量
PROJECT_NAME="easemob-doc-mcp"
PROJECT_DIR="/opt/$PROJECT_NAME"
GITHUB_REPO="https://github.com/dujiepeng/easemob-doc-mcp.git"
SERVICE_USER="www-data"
VENV_DIR="$PROJECT_DIR/venv"

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

# 检查是否为root用户
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "检测到root用户，建议使用普通用户运行此脚本"
        read -p "是否继续？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# 检查系统要求
check_system() {
    print_info "检查系统要求..."
    
    # 检查操作系统
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        print_error "无法检测操作系统"
        exit 1
    fi
    
    print_info "操作系统: $OS $VER"
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 未安装"
        print_info "正在安装Python3..."
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_info "Python版本: $PYTHON_VERSION"
    
    # 检查Git
    if ! command -v git &> /dev/null; then
        print_info "安装Git..."
        sudo apt update
        sudo apt install -y git
    fi
    
    # 检查curl
    if ! command -v curl &> /dev/null; then
        print_info "安装curl..."
        sudo apt update
        sudo apt install -y curl
    fi
}

# 创建项目目录
setup_project() {
    print_info "设置项目目录..."
    
    # 创建项目目录
    sudo mkdir -p $PROJECT_DIR
    sudo chown $USER:$USER $PROJECT_DIR
    
    # 如果目录已存在且有内容，询问是否覆盖
    if [[ -d "$PROJECT_DIR/src" ]]; then
        print_warning "项目目录已存在"
        read -p "是否重新下载项目？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf $PROJECT_DIR/*
        else
            print_info "使用现有项目文件"
            return
        fi
    fi
    
    # 下载项目文件
    print_info "下载项目文件..."
    if [[ -d ".git" ]]; then
        # 如果在项目目录中，直接复制
        cp -r . $PROJECT_DIR/
    else
        # 从GitHub下载
        git clone $GITHUB_REPO $PROJECT_DIR
    fi
    
    cd $PROJECT_DIR
}

# 创建虚拟环境
setup_venv() {
    print_info "创建虚拟环境..."
    
    cd $PROJECT_DIR
    
    # 检查并安装python3-venv
    if ! dpkg -l | grep -q python3-venv; then
        print_info "安装python3-venv..."
        sudo apt update
        sudo apt install -y python3-venv
    fi
    
    # 创建虚拟环境
    if command -v python3.12 &> /dev/null; then
        print_info "使用Python 3.12创建虚拟环境..."
        python3.12 -m venv $VENV_DIR
    elif command -v python3.11 &> /dev/null; then
        print_info "使用Python 3.11创建虚拟环境..."
        python3.11 -m venv $VENV_DIR
    elif command -v python3.10 &> /dev/null; then
        print_info "使用Python 3.10创建虚拟环境..."
        python3.10 -m venv $VENV_DIR
    else
        print_info "使用默认Python3创建虚拟环境..."
        python3 -m venv $VENV_DIR
    fi
    
    # 检查虚拟环境是否创建成功
    if [[ ! -f "$VENV_DIR/bin/python" ]]; then
        print_error "虚拟环境创建失败"
        exit 1
    fi
    
    print_success "虚拟环境创建成功"
}

# 安装依赖
install_dependencies() {
    print_info "安装Python依赖..."
    
    cd $PROJECT_DIR
    source $VENV_DIR/bin/activate
    
    # 升级pip
    pip install --upgrade pip
    
    # 安装项目依赖
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
    else
        print_warning "requirements.txt不存在，安装基本依赖..."
        pip install fastmcp>=2.9.0
    fi
    
    print_success "依赖安装完成"
}

# 创建systemd服务
create_service() {
    print_info "创建systemd服务..."
    
    # 创建服务文件
    cat > /tmp/easemob-doc-mcp.service << EOF
[Unit]
Description=环信文档搜索 MCP 服务
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$VENV_DIR/bin
ExecStart=$VENV_DIR/bin/python src/server.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    # 安装服务
    sudo cp /tmp/easemob-doc-mcp.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable easemob-doc-mcp
    
    print_success "systemd服务创建完成"
}

# 启动服务
start_service() {
    print_info "启动服务..."
    
    sudo systemctl start easemob-doc-mcp
    
    # 等待服务启动
    sleep 3
    
    # 检查服务状态
    if sudo systemctl is-active --quiet easemob-doc-mcp; then
        print_success "服务启动成功！"
    else
        print_error "服务启动失败"
        sudo systemctl status easemob-doc-mcp
        exit 1
    fi
}

# 测试服务
test_service() {
    print_info "测试服务..."
    
    # 等待服务完全启动
    sleep 5
    
    # 测试MCP端点
    if curl -s http://localhost:9000/mcp/ > /dev/null; then
        print_success "服务测试通过！"
    else
        print_warning "服务测试失败，但服务可能仍在启动中"
    fi
}

# 显示完成信息
show_completion() {
    echo
    print_success "=== 部署完成 ==="
    echo
    echo "项目信息:"
    echo "  项目目录: $PROJECT_DIR"
    echo "  虚拟环境: $VENV_DIR"
    echo "  服务名称: easemob-doc-mcp"
    echo
    echo "服务管理:"
    echo "  查看状态: sudo systemctl status easemob-doc-mcp"
    echo "  启动服务: sudo systemctl start easemob-doc-mcp"
    echo "  停止服务: sudo systemctl stop easemob-doc-mcp"
    echo "  重启服务: sudo systemctl restart easemob-doc-mcp"
    echo "  查看日志: sudo journalctl -u easemob-doc-mcp -f"
    echo
    echo "服务地址:"
    echo "  HTTP: http://$(hostname -I | awk '{print $1}'):9000"
    echo "  MCP: http://$(hostname -I | awk '{print $1}'):9000/mcp/"
    echo
    echo "Cursor配置:"
    echo "  在Cursor的MCP配置中添加:"
    echo "  {"
    echo "    \"easemob-doc-mcp\": {"
    echo "      \"transport\": \"http\","
    echo "      \"url\": \"http://$(hostname -I | awk '{print $1}'):9000/mcp/\""
    echo "    }"
    echo "  }"
    echo
    print_success "部署完成！服务已自动启动并设置为开机自启。"
}

# 主函数
main() {
    echo -e "${GREEN}"
    echo "=========================================="
    echo "  环信文档搜索 MCP 服务一键部署脚本"
    echo "=========================================="
    echo -e "${NC}"
    
    check_root
    check_system
    setup_project
    setup_venv
    install_dependencies
    create_service
    start_service
    test_service
    show_completion
}

# 错误处理
trap 'print_error "部署过程中发生错误，请检查日志"; exit 1' ERR

# 运行主函数
main "$@" 