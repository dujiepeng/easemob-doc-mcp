#!/bin/bash

# 快速部署脚本 - 解决服务器环境问题

set -e

echo "=== 环信文档搜索 MCP 服务快速部署 ==="

# 1. 安装系统依赖
echo "1. 安装系统依赖..."
sudo apt update
sudo apt install -y python3-venv python3-pip

# 2. 检查Python版本
echo "2. 检查Python版本..."
python3 --version

# 3. 创建项目目录
PROJECT_DIR="/opt/easemob-doc-mcp"
echo "3. 创建项目目录: $PROJECT_DIR"
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# 4. 复制项目文件
echo "4. 复制项目文件..."
cp -r . $PROJECT_DIR/
cd $PROJECT_DIR

# 5. 创建虚拟环境
echo "5. 创建虚拟环境..."
python3 -m venv venv

# 6. 激活虚拟环境并安装依赖
echo "6. 安装Python依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 7. 测试运行
echo "7. 测试运行..."
python src/server.py &
SERVER_PID=$!

# 等待服务器启动
sleep 5

# 检查服务器是否正常运行
if curl -s http://localhost:9000/mcp/ > /dev/null; then
    echo "✅ 服务器启动成功！"
    echo "服务运行在: http://localhost:9000"
    echo "MCP端点: http://localhost:9000/mcp/"
else
    echo "❌ 服务器启动失败"
fi

# 停止测试服务器
kill $SERVER_PID 2>/dev/null || true

echo ""
echo "=== 部署完成 ==="
echo "项目目录: $PROJECT_DIR"
echo "虚拟环境: $PROJECT_DIR/venv"
echo ""
echo "手动启动服务:"
echo "cd $PROJECT_DIR && source venv/bin/activate && python src/server.py"
echo ""
echo "或者运行完整部署脚本: ./deploy.sh" 