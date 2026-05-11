"""
阿里云百炼 STT 语音识别 - 使用 Paraformer 实时识别
支持本地 wav 文件
"""
import os
import base64
import json
import tempfile
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

stt_router = APIRouter()


@stt_router.post("/stream")
async def stream_stt():
    """阿里云百炼流式语音识别（已弃用）"""
    return JSONResponse({"status": "deprecated"})


@stt_router.post("/transcribe")
async def transcribe_audio(request: Request):
    """使用阿里云百炼 Paraformer 转录音频（支持本地文件）"""
    try:
        body = await request.body()
        
        # 尝试解析 JSON
        try:
            data = json.loads(body)
            audio_base64 = data.get("audio", "")
        except:
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
        
        # 使用阿里云百炼实时识别 API
        import dashscope
        from dashscope.audio.asr import Recognition
        
        dashscope.api_key = DASHSCOPE_API_KEY
        
        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav', mode='wb') as f:
            f.write(audio_data)
            temp_file = f.name
        
        try:
            # 调用 Paraformer 实时识别
            recognition = Recognition(model='paraformer-realtime-v2')
            result = recognition.call(temp_file)
            
            if result.status_code != 200:
                return {"transcript": "", "error": result.message}
            
            # 提取文本
            if hasattr(result, 'text') and result.text:
                return {"transcript": result.text}
            
            return {"transcript": ""}
            
        finally:
            try:
                os.unlink(temp_file)
            except:
                pass
                
    except Exception as e:
        print(f"STT error: {e}")
        return {"transcript": "", "error": str(e)}