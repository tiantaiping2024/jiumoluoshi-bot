"""
阿里云百炼 STT 语音识别 - 使用 Paraformer
"""
import os
import base64
import json
import asyncio
import aiohttp
import tempfile
import shutil
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

stt_router = APIRouter()


@stt_router.post("/stream")
async def stream_stt():
    """阿里云百炼流式语音识别"""
    return JSONResponse({"status": "deprecated"})


@stt_router.post("/transcribe")
async def transcribe_audio(request: Request):
    """使用阿里云百炼 Paraformer 转录音频"""
    try:
        body = await request.body()
        
        # 尝试解析 JSON
        try:
            data = json.loads(body)
            audio_base64 = data.get("audio", "")
        except:
            # 直接是 base64 数据
            audio_base64 = body.decode("utf-8", errors="ignore")
        
        if not audio_base64:
            raise HTTPException(status_code=400, detail="No audio provided")
        
        # 解码音频
        try:
            if "," in audio_base64:
                audio_base64 = audio_base64.split(",")[1]
            audio_data = base64.b64decode(audio_base64)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid audio data: {e}")
        
        if not DASHSCOPE_API_KEY:
            return {"transcript": "", "error": "DASHSCOPE_API_KEY not configured"}
        
        # 使用阿里云百炼 Paraformer
        import dashscope
        from dashscope import MultiModalConversation
        
        dashscope.api_key = DASHSCOPE_API_KEY
        
        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav', mode='wb') as f:
            f.write(audio_data)
            temp_file = f.name
        
        try:
            # 调用 Paraformer
            resp = MultiModalConversation.call(
                model='paraformer-realtime-v2',
                messages=[{
                    'role': 'user',
                    'content': [{'audio': f'file://{temp_file}'}]
                }],
                stream=False
            )
            
            if resp.get("status_code") != 200:
                return {"transcript": "", "error": resp.get('message', 'Unknown error')}
            
            # 提取文本
            output = resp.get("output", {})
            choices = output.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                content = message.get("content", [])
                if content:
                    transcript = content[0].get("text", "")
                    return {"transcript": transcript}
            
            return {"transcript": ""}
            
        finally:
            # 删除临时文件
            try:
                os.unlink(temp_file)
            except:
                pass
                
    except Exception as e:
        print(f"STT error: {e}")
        return {"transcript": "", "error": str(e)}
