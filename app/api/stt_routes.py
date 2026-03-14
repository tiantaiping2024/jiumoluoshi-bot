"""
Deepgram STT 语音识别 - 流式识别
"""
import os
import base64
import json
import asyncio
import aiohttp
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")

stt_router = APIRouter()


@stt_router.post("/api/stt/stream")
async def stream_stt():
    """Deepgram 流式语音识别接口"""
    return JSONResponse({"status": "deprecated"})


@stt_router.post("/api/stt/transcribe")
async def transcribe_audio(request: Request):
    """使用 Deepgram 转录音频"""
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
        
        if not DEEPGRAM_API_KEY:
            return {"transcript": "", "error": "Deepgram API key not configured"}
        
        # 检测音频格式
        content_type = "audio/webm" if audio_data[:4] == b'\x1aE' else "audio/wav"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.deepgram.com/v1/listen",
                headers={
                    "Authorization": f"Token {DEEPGRAM_API_KEY}",
                    "Content-Type": content_type
                },
                params={
                    "punctuate": "true",
                    "language": "zh-CN",
                    "model": "nova-2"
                },
                data=audio_data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    if result.get("results", {}).get("channels"):
                        transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
                        return {"transcript": transcript}
                
                return {"transcript": "", "error": f"Deepgram error: {resp.status}"}
                
    except Exception as e:
        print(f"STT error: {e}")
        return {"transcript": "", "error": str(e)}
