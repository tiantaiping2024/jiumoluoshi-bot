"""
Edge TTS 语音合成模块 - 鸠摩罗什高僧苍老声音
使用微软免费 Edge TTS 服务
"""
import asyncio
from base64 import b64encode
import edge_tts


DEFAULT_VOICE = "zh-CN-YunxiNeural"


async def synthesize_speech_async(text: str, voice: str = DEFAULT_VOICE, rate: str = "-15%", pitch: str = "-10Hz") -> bytes:
    """异步合成语音"""
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    
    return audio_data


async def synthesize_speech_base64_async(text: str) -> str:
    """异步接口"""
    audio_data = await synthesize_speech_async(
        text, 
        voice="zh-CN-YunxiNeural",
        rate="-15%",
        pitch="-10Hz"
    )
    return b64encode(audio_data).decode('utf-8')


# 同步版本（尽量避免使用）
def synthesize_speech_base64(text: str) -> str:
    """同步封装 - 不推荐在 async 上下文中使用"""
    return asyncio.run(synthesize_speech_base64_async(text))


def synthesize_speech_wav_base64(text: str) -> str:
    """兼容接口"""
    return synthesize_speech_base64(text)
