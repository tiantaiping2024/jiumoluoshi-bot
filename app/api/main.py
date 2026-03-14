"""
鸠摩罗什Bot API 接口 (Agent版)
"""
import os
import hashlib
import time
import xml.etree.ElementTree as ET
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path

# 导入 Agent (新版本)
from app.agents import create_jiumo_agent

# 导入记忆模块
from app.memory import memory

app = FastAPI(title="鸠摩罗什Bot API", version="2.0.0")

# 企业微信配置
WECHAT_CONFIG = {
    "corp_id": os.getenv("WECHAT_CORP_ID", "ww47ae0142fcfd5800"),
    "token": os.getenv("WECHAT_TOKEN", "8puiDV37qRviax0b8QG1IDeqfqQ"),
    "encoding_aes_key": os.getenv("WECHAT_ENCODING_AES_KEY", "NRo67SYEcfLr1G1MWMS5pd8c2BzIbLRJiiZon68x3wj"),
    "agent_id": os.getenv("WECHAT_AGENT_ID", "1000004"),
}

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.parent.parent

# 初始化 Agent
jiumo_agent = None

def get_agent():
    """获取 Agent 实例"""
    global jiumo_agent
    if jiumo_agent is None:
        jiumo_agent = create_jiumo_agent()
    return jiumo_agent

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
    """对话接口 (Agent模式)"""
    try:
        agent = get_agent()
        
        # 加载会话历史
        history = memory.get_history(request.session_id, limit=10)
        agent.conversation_history = history
        
        # 调用 Agent
        reply = agent.chat(request.message, session_id=request.session_id)
        
        # 保存对话
        memory.save_message(request.session_id, "user", request.message)
        memory.save_message(request.session_id, "assistant", reply)
        
        return ChatResponse(reply=reply, session_id=request.session_id)
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Chat error: {e}\n{error_detail}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/clear")
async def clear_session(session_id: str = "default"):
    """清空会话"""
    memory.clear(session_id)
    agent = get_agent()
    agent.clear_history()
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
    return {"status": "healthy", "name": "鸠摩罗什Bot Agent", "version": "2.0.0"}

# ========== 阿里云百炼 TTS 接口 ==========
import os

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
TTS_VOICE = "Ryan"  # 成熟男声

@api_router.post("/tts")
async def text_to_speech(text: str):
    """将文本转换为语音 (阿里云百炼 Qwen3-TTS)"""
    try:
        from app.tools.tts import synthesize_speech
        
        # 使用阿里云百炼 TTS 生成语音
        audio_data = synthesize_speech(text, voice=TTS_VOICE)
        
        if not audio_data:
            raise Exception("No audio generated")
        
        # 返回音频文件
        from fastapi.responses import Response
        return Response(
            content=audio_data,
            media_type="audio/wav",
            headers={"Content-Disposition": f"inline; filename=tts.wav"}
        )
    except Exception as e:
        print(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

@api_router.get("/voices")
async def list_voices():
    """列出可用的阿里云百炼 TTS 语音"""
    return {
        "voices": [
            {"name": "Ethan", "gender": "male", "description": "Ethan - 苍老男声"},
            {"name": "Dylan", "gender": "male", "description": "Dylan - 男声"},
            {"name": "Alex", "gender": "male", "description": "Alex - 男声"},
            {"name": "Ryan", "gender": "male", "description": "Ryan - 男声"},
            {"name": "Daniel", "gender": "male", "description": "Daniel - 男声"},
            {"name": "Cherry", "gender": "female", "description": "Cherry - 女声"},
            {"name": "Sunny", "gender": "female", "description": "Sunny - 女声"},
            {"name": "Amy", "gender": "female", "description": "Amy - 女声"},
            {"name": "Luna", "gender": "female", "description": "Luna - 女声"},
            {"name": "Jessica", "gender": "female", "description": "Jessica - 女声"},
        ]
    }

@api_router.get("/tools")
async def list_tools():
    """列出可用工具"""
    agent = get_agent()
    return {
        "tools": [
            {"name": t.name, "description": t.description}
            for t in agent.tools
        ]
    }

# ========== 企业微信回调接口 ==========
def verify_wechat_signature(token: str, timestamp: str, nonce: str, echostr: str = "") -> str:
    """验证企业微信签名"""
    sorted_params = sorted([token, timestamp, nonce, echostr])
    signature = hashlib.sha1("".join(sorted_params).encode()).hexdigest()
    return signature

@app.get("/api/wechat")
async def wechat_verify(
    msg_signature: str = Query(""),
    timestamp: str = Query(""),
    nonce: str = Query(""),
    echostr: str = Query("")
):
    """企业微信验证回调 - 用于首次配置验证"""
    if echostr:
        return PlainTextResponse(content=echostr)
    return PlainTextResponse(content="success")

@app.post("/api/wechat")
async def wechat_message(request: Request, msg_signature: str = Query(""), timestamp: str = Query(""), nonce: str = Query("")):
    """企业微信消息接收"""
    try:
        body = await request.body()
        xml_str = body.decode('utf-8')
        
        # 解析XML
        root = ET.fromstring(xml_str)
        msg_type = root.find("MsgType").text
        from_user = root.find("FromUserName").text
        content = root.find("Content").text if root.find("Content") is not None else ""
        
        # 生成回复
        if msg_type == "text":
            session_id = f"wechat_{from_user}"
            
            # 获取对话历史
            agent = get_agent()
            history = memory.get_history(session_id, limit=10)
            agent.conversation_history = history
            
            # 调用 Agent
            reply = agent.chat(content, session_id=session_id)
            
            # 保存对话
            memory.save_message(session_id, "user", content)
            memory.save_message(session_id, "assistant", reply)
            
            # 返回XML响应
            response_xml = f"""<xml>
<ToUserName><![CDATA[{from_user}]]></ToUserName>
<FromUserName><![CDATA[{WECHAT_CONFIG['corp_id']}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{reply}]]></Content>
</xml>"""
            return PlainTextResponse(content=response_xml)
        
        return PlainTextResponse(content="success")
    except Exception as e:
        print(f"WeChat error: {e}")
        return PlainTextResponse(content="success")

# 注册API路由
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
