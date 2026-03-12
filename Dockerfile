FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY app/ ./app/
COPY web/ ./web/
COPY soul.md .
COPY config/ ./config/

# 设置环境变量
ENV DEEPSEEK_API_KEY=sk-b2bc78855f1b4b21978532f879bc718f

# 创建数据目录
RUN mkdir -p data/memories

# 暴露端口
EXPOSE 8000

# 启动
CMD ["python", "-m", "app.api.main"]
