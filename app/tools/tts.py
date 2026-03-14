"""
阿里云 DashScope TTS 语音合成模块 - 鸠摩罗什高僧苍老声音
使用阿里云百炼 Qwen3-TTS 服务
支持情感控制和动作描述过滤
"""
import os
import re
import requests
from base64 import b64encode


DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
TTS_MODEL = "qwen3-tts-flash"

# 可用的中文声音
VOICES = {
    "Ethan": "Ethan - 成熟男声",
    "Ryan": "Ryan - 男声",
    "Dylan": "Dylan - 男声",
    "Alex": "Alex - 男声",
    "Daniel": "Daniel - 男声",
    "Arnold": "Arnold - 成熟男声",
    "Jeremy": "Jeremy - 男声",
    "Matthew": "Matthew - 男声",
}

DEFAULT_VOICE = "Bodega"  # 男性音色


def filter_action_descriptions(text: str) -> str:
    """过滤掉动作描述，只保留对话内容"""
    # 移除 [xxx]、(xxx)、【xxx】等动作描述
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'【.*?】', '', text)
    # 清理多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def synthesize_speech(text: str, voice: str = DEFAULT_VOICE, format: str = "wav", 
                       emotion: str = "neutral", rate: float = 1.0, pitch: float = 0) -> bytes:
    """使用阿里云百炼 TTS 合成语音"""
    if not DASHSCOPE_API_KEY:
        raise Exception("DASHSCOPE_API_KEY 未配置")
    
    # 过滤动作描述
    text = filter_action_descriptions(text)
    
    if not text:
        text = "你好"
    
    try:
        import dashscope
        from dashscope import MultiModalConversation
        
        dashscope.api_key = DASHSCOPE_API_KEY
        
        # 使用 SSML 添加情感控制
        # emotion: happy, sad, angry, neutral
        ssml_text = f"<speak><voice name='{voice}'><prosody rate='{rate}' pitch='{pitch}'>{text}</prosody></voice></speak>"
        
        # 调用 TTS
        resp = MultiModalConversation.call(
            model=TTS_MODEL,
            text=ssml_text,  # 使用 SSML
            voice=voice,
            stream=False
        )
        
        if resp.get("status_code") != 200:
            # 如果 SSML 不支持，回退到普通文本
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


def synthesize_speech_base64(text: str, emotion: str = "neutral") -> str:
    """返回 Base64 编码的音频"""
    # 更慢、更低沉的苍老声音
    rate = 0.8  # 慢速，更稳重
    pitch = -3  # 更低的音调，更苍老
    
    if emotion == "happy":
        rate = 0.9
        pitch = -1
    elif emotion == "sad":
        rate = 0.7
        pitch = -4
    
    audio_data = synthesize_speech(text, rate=rate, pitch=pitch)
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
