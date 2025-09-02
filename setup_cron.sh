#!/bin/bash

# 环信文档更新定时任务设置脚本
# 设置每天自动从GitHub拉取最新文档

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UPDATE_SCRIPT="$PROJECT_DIR/update_docs.sh"

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

# 检查脚本是否存在
check_script() {
    if [ ! -f "$UPDATE_SCRIPT" ]; then
        print_error "更新脚本不存在: $UPDATE_SCRIPT"
        exit 1
    fi
    
    # 确保脚本有执行权限
    chmod +x "$UPDATE_SCRIPT"
}

# 设置定时任务
setup_cron() {
    print_info "设置每日定时更新任务..."
    
    # 默认设置为每天凌晨3点执行
    CRON_TIME="0 3 * * *"
    
    # 检查是否已存在相同的定时任务
    EXISTING_CRON=$(crontab -l 2>/dev/null | grep -F "$UPDATE_SCRIPT" || true)
    
    if [ -n "$EXISTING_CRON" ]; then
        print_warning "已存在相关定时任务:"
        echo "$EXISTING_CRON"
        read -p "是否要替换现有任务? (y/n): " REPLACE
        if [ "$REPLACE" != "y" ] && [ "$REPLACE" != "Y" ]; then
            print_info "保留现有定时任务"
            return
        fi
        
        # 删除现有任务
        crontab -l 2>/dev/null | grep -v "$UPDATE_SCRIPT" | crontab -
    fi
    
    # 添加新的定时任务
    (crontab -l 2>/dev/null; echo "$CRON_TIME $UPDATE_SCRIPT >> $PROJECT_DIR/update_docs.log 2>&1") | crontab -
    
    print_success "定时任务设置成功！每天凌晨3点自动更新文档"
}

# 显示定时任务信息
show_cron_info() {
    print_info "当前定时任务列表:"
    crontab -l | grep -v "^#" || echo "没有设置定时任务"
    
    print_info "定时任务日志文件: $PROJECT_DIR/update_docs.log"
}

# 主函数
main() {
    echo -e "${GREEN}"
    echo "========================================"
    echo "  环信文档更新定时任务设置"
    echo "========================================"
    echo -e "${NC}"
    
    check_script
    setup_cron
    show_cron_info
    
    print_success "设置完成！"
    print_info "您可以通过以下命令手动执行更新:"
    echo "  $UPDATE_SCRIPT"
}

# 运行主函数
main
