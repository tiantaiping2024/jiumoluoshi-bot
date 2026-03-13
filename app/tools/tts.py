"""
Edge TTS 语音合成模块 - 鸠摩罗什高僧苍老声音
使用微软免费 Edge TTS 服务
"""
import asyncio
import io
import wave
import json
from base64 import b64encode
import edge_tts
from edge_tts import Communicate


# 可用的中文男声（苍老/低沉）
VOICES = {
    # 苍老男声推荐
    "zh-CN-YunxiNeural": "云希 - 青年男声",
    "zh-CN-YunyangNeural": "云扬 - 标准男声", 
    "zh-CN-XiaoxiaoNeural": "晓晓 - 女声",
    "zh-CN-XiaoyiNeural": "晓伊 - 女声",
    # 其他可选
    "zh-HK-HiuGaaiNeural": "香港女声",
    "zh-TW-HsiaoChenNeural": "台湾女声",
}

# 选择苍老声音：Yunxi 比较接近，但 edge-tts 没有真正的老年声音
# 可以通过调整语速和音调来模拟
DEFAULT_VOICE = "zh-CN-YunxiNeural"


async def synthesize_speech_async(text: str, voice: str = DEFAULT_VOICE, rate: str = "-10%", pitch: str = "-10Hz") -> bytes:
    """
    异步合成语音
    
    Args:
        text: 要转换的文本
        voice: 语音名称
        rate: 语速调整，如 "-10%" 表示减慢10%
        pitch: 音调调整，如 "-10Hz" 表示降低10Hz
    
    Returns:
        WAV 音频数据
    """
    # 调整参数让声音更低沉、缓慢（像高僧）
    communicate = Communicate(text, voice, rate=rate, pitch=pitch)
    
    # 收集音频数据
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    
    return audio_data


def synthesize_speech_wav_base64(text: str) -> str:
    """
    合成语音，返回 WAV 格式 Base64 - 鸠摩罗什苍老僧人声音
    """
    # 使用云希声音，调整参数使其更低沉缓慢
    # rate: -15% 较慢，pitch: -10Hz 较低
    audio_data = asyncio.run(synthesize_speech_async(
        text, 
        voice="zh-CN-YunxiNeural",
        rate="-15%",      # 较慢，像高僧讲话
        pitch="-10Hz"     # 较低沉
    ))
    
    # 如果是 MP3，转为 WAV
    # edge-tts 返回的是 MP3，需要转换
    from pydub import AudioSegment
    
    audio_file = io.BytesIO(audio_data)
    try:
        sound = AudioSegment.from_file(audio_file, format="mp3")
        
        # 转为 WAV 格式
        wav_buffer = io.BytesIO()
        sound.export(wav_buffer, format="wav")
        wav_data = wav_buffer.getvalue()
    except Exception as e:
        # 如果转换失败，直接返回原始数据
        print(f"音频转换错误: {e}")
        wav_data = audio_data
    
    return b64encode(wav_data).decode('utf-8')


def synthesize_speech_base64(text: str) -> str:
    """兼容旧接口"""
    return synthesize_speech_wav_base64(text)


# 测试
if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "阿弥陀佛，施主你好贫衲是鸠摩罗什"
    result = synthesize_speech_wav_base64(text)
    print(f"Generated {len(result)} chars base64")
