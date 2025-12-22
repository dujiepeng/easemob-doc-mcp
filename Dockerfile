FROM python:3.11-slim-bookworm

# 设置工作目录
WORKDIR /app

# 安装系统依赖
# 替换为清华大学镜像源 (Debian Bookworm)
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list \
    && apt-get update && apt-get install -y \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
COPY src/ ./src/
COPY pyproject.toml .

# 安装Python依赖 (使用清华源加速)
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 暴露端口
EXPOSE 9000

# 启动命令
CMD ["python", "src/server.py"] 