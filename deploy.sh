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

# 1. 创建项目目录
echo "创建项目目录..."
sudo mkdir -p $PROJECT_DIR
sudo chown $SERVICE_USER:$SERVICE_USER $PROJECT_DIR

# 2. 复制项目文件
echo "复制项目文件..."
cp -r . $PROJECT_DIR/
sudo chown -R $SERVICE_USER:$SERVICE_USER $PROJECT_DIR

# 3. 创建虚拟环境
echo "创建虚拟环境..."
cd $PROJECT_DIR
sudo -u $SERVICE_USER python3 -m venv $VENV_DIR
sudo -u $SERVICE_USER $VENV_DIR/bin/pip install --upgrade pip
sudo -u $SERVICE_USER $VENV_DIR/bin/pip install -r requirements.txt

# 4. 更新服务文件路径
echo "配置服务文件..."
sed -i "s|/path/to/easemob-doc-mcp|$PROJECT_DIR|g" $SERVICE_FILE
sed -i "s|/path/to/venv|$VENV_DIR|g" $SERVICE_FILE

# 5. 安装 systemd 服务
echo "安装 systemd 服务..."
sudo cp $SERVICE_FILE /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $PROJECT_NAME

# 6. 启动服务
echo "启动服务..."
sudo systemctl start $PROJECT_NAME
sudo systemctl status $PROJECT_NAME

echo "部署完成！"
echo "服务状态: sudo systemctl status $PROJECT_NAME"
echo "查看日志: sudo journalctl -u $PROJECT_NAME -f"
echo "重启服务: sudo systemctl restart $PROJECT_NAME" 