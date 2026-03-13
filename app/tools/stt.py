"""
Deepgram 语音识别模块
"""
import os
import asyncio
import base64
from deepgram import Deepgram


DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")


async def transcribe_audio_async(audio_data: bytes, language: str = "zh-CN") -> str:
    """使用 Deepgram 转录音频"""
    if not DEEPGRAM_API_KEY:
        return ""
    
    try:
        deepgram = Deepgram(DEEPGRAM_API_KEY)
        
        # 创建虚拟文件
        buffer = audio_data
        
        response = await deepgram.transcription.prerecorded(
            buffer,
            {
                "punctuate": True,
                "language": language,
                "model": "nova-2",
            }
        )
        
        # 提取转录文本
        if response["results"]["channels"]:
            transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
            return transcript
        
        return ""
    except Exception as e:
        print(f"Deepgram 转录错误: {e}")
        return ""


def transcribe_audio(audio_data: bytes, language: str = "zh-CN") -> str:
    """同步封装"""
    try:
        return asyncio.run(transcribe_audio_async(audio_data, language))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(transcribe_audio_async(audio_data, language))


async def transcribe_base64_async(audio_base64: str, language: str = "zh-CN") -> str:
    """从 Base64 转录音频"""
    if not audio_base64:
        return ""
    
    try:
        # 解码 Base64
        audio_data = base64.b64decode(audio_base64)
        return await transcribe_audio_async(audio_data, language)
    except Exception as e:
        print(f"Base64 转录错误: {e}")
        return ""
