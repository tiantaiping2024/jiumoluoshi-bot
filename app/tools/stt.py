"""
Deepgram 语音识别模块 - 使用 REST API (免费额度)
"""
import os
import requests


DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
DEEPGRAM_URL = "https://api.deepgram.com/v1/listen"


def transcribe_audio(audio_data: bytes, language: str = "zh-CN") -> str:
    """使用 Deepgram REST API 转录音频"""
    if not DEEPGRAM_API_KEY:
        return ""
    
    try:
        # 检测音频格式
        content_type = "audio/webm" if audio_data[:4] == b'\x1aE' else "audio/wav"
        
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": content_type
        }
        
        params = {
            "punctuate": "true",
            "language": language,
            "model": "nova-2"
        }
        
        response = requests.post(
            DEEPGRAM_URL,
            headers=headers,
            params=params,
            data=audio_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("results", {}).get("channels"):
                transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
                return transcript
        
        return ""
    except Exception as e:
        print(f"Deepgram 转录错误: {e}")
        return ""


def transcribe_base64(audio_base64: str, language: str = "zh-CN") -> str:
    """从 Base64 转录音频"""
    if not audio_base64:
        return ""
    
    try:
        import base64
        audio_data = base64.b64decode(audio_base64)
        return transcribe_audio(audio_data, language)
    except Exception as e:
        print(f"Base64 转录错误: {e}")
        return ""


async def transcribe_audio_async(audio_data: bytes, language: str = "zh-CN") -> str:
    """异步封装"""
    return transcribe_audio(audio_data, language)


async def transcribe_base64_async(audio_base64: str, language: str = "zh-CN") -> str:
    """异步封装"""
    return transcribe_base64(audio_base64, language)
