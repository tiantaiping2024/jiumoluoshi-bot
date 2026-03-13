"""
Edge TTS 语音合成模块 - 鸠摩罗什高僧苍老声音
使用微软免费 Edge TTS 服务
"""
import asyncio
import io
from base64 import b64encode
import edge_tts


# 可用的中文男声
DEFAULT_VOICE = "zh-CN-YunxiNeural"


async def synthesize_speech_async(text: str, voice: str = DEFAULT_VOICE, rate: str = "-15%", pitch: str = "-10Hz") -> bytes:
    """
    异步合成语音，返回 MP3 音频数据
    """
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    
    return audio_data


def synthesize_speech_wav_base64(text: str) -> str:
    """
    合成语音，返回 Base64 - 鸠摩罗什苍老僧人声音
    """
    audio_data = asyncio.run(synthesize_speech_async(
        text, 
        voice="zh-CN-YunxiNeural",
        rate="-15%",
        pitch="-10Hz"
    ))
    
    return b64encode(audio_data).decode('utf-8')


def synthesize_speech_base64(text: str) -> str:
    """兼容旧接口"""
    return synthesize_speech_wav_base64(text)


# 测试
if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "阿弥陀佛，施主你好"
    result = synthesize_speech_wav_base64(text)
    print(f"Generated {len(result)} chars base64")
