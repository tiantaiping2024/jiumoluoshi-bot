"""
鸠摩罗什Bot API 接口
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path

from app.core.chat_engine import chat_engine
from app.memory import memory

app = FastAPI(title="鸠摩罗什Bot API", version="1.0.0")

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.parent.parent

# 根路径返回前端页面
@app.get("/")
async def root():
    return FileResponse(ROOT_DIR / "web" / "index.html")

# 挂载静态前端
app.mount("/static", StaticFiles(directory=str(ROOT_DIR / "web")), name="static")

# API路由
api_router = APIRouter(prefix="/api")

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    use_knowledge: bool = True

class ChatResponse(BaseModel):
    reply: str
    session_id: str

@api_router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """对话接口"""
    try:
        history = memory.get_history(request.session_id, limit=10)
        chat_engine.conversation_history = history
        reply = chat_engine.chat(request.message, use_knowledge=request.use_knowledge)
        memory.save_message(request.session_id, "user", request.message)
        memory.save_message(request.session_id, "assistant", reply)
        return ChatResponse(reply=reply, session_id=request.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/clear")
async def clear_session(session_id: str = "default"):
    """清空会话"""
    memory.clear(session_id)
    return {"status": "ok", "message": "会话已清空"}

@api_router.get("/history")
async def get_history(session_id: str = "default", limit: int = 10):
    """获取会话历史"""
    history = memory.get_history(session_id, limit=limit)
    return {"session_id": session_id, "history": history}

@api_router.get("/profile")
async def get_profile(session_id: str = "default"):
    """获取用户画像"""
    profile = memory.get_profile(session_id)
    return {"session_id": session_id, "profile": profile}

@api_router.post("/profile")
async def update_profile(session_id: str = "default", key: str = None, value: str = None):
    """更新用户画像"""
    if key and value:
        memory.add_user_profile(session_id, key, value)
    return {"status": "ok"}

@api_router.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy", "name": "鸠摩罗什Bot"}

# 注册API路由
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
