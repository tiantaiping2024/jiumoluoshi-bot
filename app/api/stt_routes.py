"""
Deepgram STT 语音识别 - 使用 REST API 直接调用
前端 MediaRecorder 采集的 webm/opus 音频流转为 base64 发送至此
"""
import os
import base64
import json
import requests
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

stt_router = APIRouter()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
DEEPGRAM_URL = "https://api.deepgram.com/v1/listen"


@stt_router.post("/transcribe")
async def transcribe_audio(request: Request):
    """使用 Deepgram 转录音频（支持 webm/opus）"""
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
        
        if not DEEPGRAM_API_KEY:
            return {"transcript": "", "error": "DEEPGRAM_API_KEY not configured"}
        
        # 直接调用 Deepgram REST API
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/webm",
        }
        params = {
            "model": "nova-2",
            "language": "zh-CN",
            "smart_format": "true",
            "punctuate": "true",
        }
        
        response = requests.post(
            DEEPGRAM_URL,
            headers=headers,
            params=params,
            data=audio_data,
            timeout=30
        )
        
        if response.status_code != 200:
            return {"transcript": "", "error": f"Deepgram error: {response.status_code} {response.text}"}
        
        result = response.json()
        
        # 提取 transcript
        transcript = ""
        try:
            for channel in result.get("results", {}).get("channels", []):
                for alternative in channel.get("alternatives", []):
                    if alternative.get("transcript"):
                        transcript += alternative["transcript"] + " "
        except Exception as e:
            return {"transcript": "", "error": f"Parse error: {e}"}
        
        transcript = transcript.strip()
        return {"transcript": transcript}
        
    except requests.exceptions.Timeout:
        return {"transcript": "", "error": "Deepgram request timeout"}
    except Exception as e:
        print(f"STT error: {e}")
        return {"transcript": "", "error": str(e)}