# 部署指南

## 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 复制配置
cp config/.env.example config/.env
# 编辑 config/.env 填入 DEEPSEEK_API_KEY

# 启动服务
python -m app.api.main
# 访问 http://localhost:8000
```

## Docker 部署

### 1. 准备服务器

需要安装：
- Docker
- Docker Compose

### 2. 配置

```bash
# 复制环境配置
cp .env.docker .env
# 编辑 .env 填入你的 DEEPSEEK_API_KEY
```

### 3. 部署

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

### 4. 访问

- HTTP: http://你的服务器IP

## 云平台部署

### Railway
```bash
railway init
railway env set DEEPSEEK_API_KEY=your-key
railway up
```

### Render
```bash
# 推送代码到 GitHub
# 在 Render 后台创建 Web Service
# 设置启动命令: python -m app.api.main
# 添加环境变量 DEEPSEEK_API_KEY
```

### Fly.io
```bash
fly launch
fly secrets set DEEPSEEK_API_KEY=your-key
fly deploy
```

## Nginx + Systemd (生产推荐)

1. 构建 Docker 镜像：
```bash
docker build -t jiumoluoshi-bot .
```

2. 使用 docker-compose.yml 部署

---

*鸠摩罗什Bot v1.0.0*
