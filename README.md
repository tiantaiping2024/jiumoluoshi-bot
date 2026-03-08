# 鸠摩罗什Bot

AI佛学翻译助手 - 以鸠摩罗什大师的身份与用户对话

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行服务

```bash
python -m app.api.main
```

服务将在 http://localhost:8000 启动

### 3. 测试对话

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "大师，什么是空性？"}'
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /chat | POST | 对话接口 |
| /clear | POST | 清空会话 |
| /history | GET | 获取历史 |
| /profile | GET/POST | 用户画像 |
| /health | GET | 健康检查 |

## 项目结构

```
jiumoluoshi-bot/
├── app/
│   ├── api/main.py         # FastAPI接口
│   ├── core/chat_engine.py # 对话引擎
│   ├── knowledge/          # 佛经知识库
│   └── memory/             # 对话记忆
├── config/                  # 配置文件
├── data/                    # 数据存储
├── soul.md                 # 人格设定
└── requirements.txt        # 依赖
```

## 功能清单

- ✅ 基础对话（DeepSeek API）
- ✅ 鸠摩罗什人格（soul.md）
- ✅ 佛经知识库（8+问答对）
- ✅ 对话历史记忆（多会话支持）
- ✅ 用户画像（自定义标签）

---

*鸠摩罗什Bot v1.0.0*
