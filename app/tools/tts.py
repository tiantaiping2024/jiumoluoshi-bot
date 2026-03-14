"""
阿里云 DashScope TTS 语音合成模块 - 鸠摩罗什高僧苍老声音
使用阿里云百炼 Qwen3-TTS 服务
"""
import os
import requests
from base64 import b64encode


DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
TTS_MODEL = "qwen3-tts-flash"

# 可用的中文声音
VOICES = {
    "Cherry": "Cherry - 女声",
    "Ethan": "Ethan - 男声", 
    "Sunny": "Sunny - 女声",
    "Dylan": "Dylan - 男声",
    "Alex": "Alex - 男声",
    "Amy": "Amy - 女声",
    "Luna": "Luna - 女声",
    "Daniel": "Daniel - 男声",
    "Jessica": "Jessica - 女声",
    "Ryan": "Ryan - 男声",
}

DEFAULT_VOICE = "Ethan"  # 苍老男声


def synthesize_speech(text: str, voice: str = DEFAULT_VOICE, format: str = "wav") -> bytes:
    """使用阿里云百炼 TTS 合成语音"""
    if not DASHSCOPE_API_KEY:
        raise Exception("DASHSCOPE_API_KEY 未配置")
    
    try:
        import dashscope
        from dashscope import MultiModalConversation
        
        dashscope.api_key = DASHSCOPE_API_KEY
        
        # 调用 TTS
        resp = MultiModalConversation.call(
            model=TTS_MODEL,
            text=text,
            voice=voice,
            stream=False
        )
        
        if resp.get("status_code") != 200:
            raise Exception(f"TTS error: {resp.get('message')}")
        
        # 获取音频 URL
        output = resp.get("output", {})
        audio = output.get("audio", {})
        audio_url = audio.get("url")
        
        if not audio_url:
            raise Exception("No audio URL returned")
        
        # 下载音频
        audio_data = requests.get(audio_url).content
        return audio_data
        
    except Exception as e:
        raise Exception(f"TTS failed: {e}")


def synthesize_speech_base64(text: str) -> str:
    """返回 Base64 编码的音频"""
    audio_data = synthesize_speech(text)
    return b64encode(audio_data).decode('utf-8')


async def synthesize_speech_async(text: str, voice: str = DEFAULT_VOICE) -> bytes:
    """异步接口"""
    import asyncio
    return await asyncio.to_thread(synthesize_speech, text, voice)


async def synthesize_speech_base64_async(text: str) -> str:
    """异步接口返回 Base64"""
    audio_data = await synthesize_speech_async(text)
    return b64encode(audio_data).decode('utf-8')


def synthesize_speech_wav_base64(text: str) -> str:
    """兼容接口"""
    return synthesize_speech_base64(text)
