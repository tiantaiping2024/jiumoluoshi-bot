FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（ChatTTS 需要）
RUN apt-get update && apt-get install -y \
    git \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 安装轻量级 torch（CPU-only，大幅减小镜像）
RUN pip install --no-cache-dir torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# 安装 ChatTTS 和其他依赖
COPY requirements.txt .
RUN pip install --no-cache-dir \
    ChatTTS \
    fastapi \
    uvicorn \
    openai \
    pydantic \
    python-dotenv \
    langchain \
    langchain-core \
    langchain-deepseek \
    langchain-community \
    langgraph \
    langchain-chroma \
    chromadb \
    langchain-text-splitters \
    tavily \
    requests \
    numpy

# 复制代码
COPY app/ ./app/
COPY web/ ./web/
COPY soul.md .
COPY config/ ./config/

# 创建数据目录
RUN mkdir -p data/memories

# 暴露端口
EXPOSE 8000

# 启动
CMD ["python", "-m", "app.api.main"]
