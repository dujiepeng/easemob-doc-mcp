#!/bin/bash

# 环信文档搜索 MCP 服务部署脚本

set -e

# 配置变量
PROJECT_NAME="easemob-doc-mcp"
PROJECT_DIR="/opt/$PROJECT_NAME"
SERVICE_USER="www-data"
VENV_DIR="/opt/$PROJECT_NAME/venv"
SERVICE_FILE="easemob-doc-mcp.service"

echo "开始部署 $PROJECT_NAME..."

# 检查Python版本
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "检测到Python版本: $PYTHON_VERSION"

# 1. 创建项目目录
echo "创建项目目录..."
sudo mkdir -p $PROJECT_DIR
sudo chown $SERVICE_USER:$SERVICE_USER $PROJECT_DIR

# 2. 复制项目文件
echo "复制项目文件..."
cp -r . $PROJECT_DIR/
sudo chown -R $SERVICE_USER:$SERVICE_USER $PROJECT_DIR

# 3. 检查并安装必要的包
echo "检查系统依赖..."
if ! dpkg -l | grep -q python3-venv; then
    echo "安装 python3-venv..."
    sudo apt update
    sudo apt install -y python3-venv python3-pip
fi

# 4. 创建虚拟环境
echo "创建虚拟环境..."
cd $PROJECT_DIR

# 尝试不同的Python版本创建虚拟环境
if command -v python3.12 &> /dev/null; then
    echo "使用 Python 3.12 创建虚拟环境..."
    sudo -u $SERVICE_USER python3.12 -m venv $VENV_DIR
elif command -v python3.11 &> /dev/null; then
    echo "使用 Python 3.11 创建虚拟环境..."
    sudo -u $SERVICE_USER python3.11 -m venv $VENV_DIR
elif command -v python3.10 &> /dev/null; then
    echo "使用 Python 3.10 创建虚拟环境..."
    sudo -u $SERVICE_USER python3.10 -m venv $VENV_DIR
else
    echo "使用默认 Python3 创建虚拟环境..."
    sudo -u $SERVICE_USER python3 -m venv $VENV_DIR
fi

# 检查虚拟环境是否创建成功
if [ ! -f "$VENV_DIR/bin/python" ]; then
    echo "错误：虚拟环境创建失败"
    echo "请确保已安装 python3-venv 包："
    echo "sudo apt install -y python3-venv"
    exit 1
fi

echo "虚拟环境创建成功"

# 5. 安装Python依赖
echo "安装Python依赖..."
sudo -u $SERVICE_USER $VENV_DIR/bin/pip install --upgrade pip
sudo -u $SERVICE_USER $VENV_DIR/bin/pip install -r requirements.txt

# 6. 更新服务文件路径
echo "配置服务文件..."
sed -i "s|/path/to/easemob-doc-mcp|$PROJECT_DIR|g" $SERVICE_FILE
sed -i "s|/path/to/venv|$VENV_DIR|g" $SERVICE_FILE

# 7. 安装 systemd 服务
echo "安装 systemd 服务..."
sudo cp $SERVICE_FILE /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $PROJECT_NAME

# 8. 启动服务
echo "启动服务..."
sudo systemctl start $PROJECT_NAME
sudo systemctl status $PROJECT_NAME

echo "部署完成！"
echo "服务状态: sudo systemctl status $PROJECT_NAME"
echo "查看日志: sudo journalctl -u $PROJECT_NAME -f"
echo "重启服务: sudo systemctl restart $PROJECT_NAME" 