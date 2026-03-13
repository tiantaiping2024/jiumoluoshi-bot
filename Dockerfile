FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（ChatTTS 需要）
RUN apt-get update && apt-get install -y \
    git \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 安装轻量级 torch（CPU-only，特定版本减小体积）
RUN pip install --no-cache-dir torch==2.1.0+cpu --index-url https://download.pytorch.org/whl/cpu/torch_stable.html

# 安装 ChatTTS 和核心依赖（不安装可选的大包）
RUN pip install --no-cache-dir \
    ChatTTS \
    fastapi \
    uvicorn \
    openai \
    pydantic \
    python-dotenv \
    numpy

# 可选依赖（按需安装）
# langchain / chromadb 等可以在运行时按需导入

# 复制代码（排除文档和大文件）
COPY app/ ./app/
COPY web/ ./web/
COPY soul.md .
COPY config/ ./config/
COPY requirements.txt .

# 创建数据目录
RUN mkdir -p data/memories

# 暴露端口
EXPOSE 8000

# 启动
CMD ["python", "-m", "app.api.main"]
