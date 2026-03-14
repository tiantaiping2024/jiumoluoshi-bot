"""
阿里云 DashScope TTS 语音合成模块 - 鸠摩罗什高僧苍老声音
使用阿里云 DashScope 语音合成服务
"""
import os
import json
import requests
from base64 import b64encode


DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
TTS_MODEL = "qwen-tts-2025-05-22"

# 可选的中文男声
VOICES = {
    "xiaogang": "小刚",
    "xiaoyun": "小云", 
    "ronnie": "罗尼",
    "chengyang": "程阳",
    "shaun": "肖恩",
}

DEFAULT_VOICE = "xiaogang"


def synthesize_speech(text: str, voice: str = DEFAULT_VOICE, format: str = "mp3") -> bytes:
    """使用阿里云 DashScope TTS 合成语音"""
    if not DASHSCOPE_API_KEY:
        raise Exception("DASHSCOPE_API_KEY 未配置")
    
    url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/generation"
    
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json",
        "X-DashScope-ApiAccept": "audio/*"
    }
    
    payload = {
        "model": TTS_MODEL,
        "input": {"text": text},
        "parameters": {
            "voice": voice,
            "format": format,
            "rate": 0.8,  # 语速
            "pitch": -2   # 音调，低一点更苍老
        }
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        # 返回二进制音频数据
        return response.content
    else:
        error = response.json()
        raise Exception(f"TTS error: {error}")


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
