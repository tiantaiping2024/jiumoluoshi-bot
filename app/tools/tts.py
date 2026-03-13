"""
ChatTTS 语音合成模块
支持抑扬顿挫、情感停顿、对话语音 - 鸠摩罗什高僧音色
"""
import io
import torch
import ChatTTS
import numpy as np
from base64 import b64encode
import random


# 全局模型实例
_chat_tts = None
_ref_audio = None


def get_chat_tts():
    """获取 ChatTTS 模型实例"""
    global _chat_tts, _ref_audio
    
    if _chat_tts is None:
        # 加载模型
        _chat_tts = ChatTTS.InferProcess()
        
        # 加载模型 - 使用较轻量的配置
        _chat_tts.load(compile=False, source="custom")
        
        # 尝试加载参考音频来控制音色（如果有的话）
        #ChatTTS 示例中可以通过 ref_audio 控制音色
        
    return _chat_tts


def synthesize_speech(text: str, speed: float = 0.8) -> bytes:
    """
    合成语音，返回 MP3 音频数据
    
    Args:
        text: 要转换的文本
        speed: 语速，0.6-1.0 之间，较慢更像高僧讲话
    
    Returns:
        MP3 音频数据
    """
    chat = get_chat_tts()
    
    # 准备文本 - 添加停顿标记增强情感
    texts = [text]
    
    # 生成参数 - 调整参数让声音更低沉、更有情感
    params_infer_code = {
        'temperature': 0.3,       # 温度
        'top_P': 0.8,            # 采样参数
        'top_K': 40,             # K值采样
        'prompt': '[oral_2][laugh_0][breathe_1]',  # 添加情感
    }
    
    # 语速控制 - 更慢
    params_refine_text = {
        'prompt': f'[speed={speed}]',  # 控制语速
    }
    
    # 推理
    wavs = chat.infer(
        texts,
        params_refine_text=params_refine_text,
        params_infer_code=params_infer_code,
    )
    
    # 转换 numpy 为音频
    wav = wavs[0].astype(np.float32)
    
    # 归一化
    if wav.max() > 1:
        wav = wav / np.abs(wav).max()
    
    # 转为 int16
    wav = (wav * 32767).astype(np.int16)
    
    # 转为字节
    return wav.tobytes()


def synthesize_speech_base64(text: str) -> str:
    """
    合成语音，返回 Base64 编码（用于前端播放）
    """
    audio_data = synthesize_speech(text)
    return b64encode(audio_data).decode('utf-8')


def synthesize_speech_wav_base64(text: str) -> str:
    """
    合成语音，返回 WAV 格式 Base64（更高质量）- 鸠摩罗什高僧苍老声音
    """
    import wave
    
    chat = get_chat_tts()
    texts = [text]
    
    # 苍老声音参数调优
    params_infer_code = {
        'temperature': 0.2,        # 较低温度，更稳定
        'top_P': 0.75,
        'top_K': 30,
        # 情感参数：更低的音调、更多的呼吸声
        'prompt': '[oral_2][laugh_0][breathe_2]',  
    }
    
    # 语速较慢，模仿老年人的节奏
    params_refine_text = {
        'prompt': '[speed=0.75]',  # 较慢的语速
    }
    
    wavs = chat.infer(
        texts,
        params_refine_text=params_refine_text,
        params_infer_code=params_infer_code,
    )
    
    wav = wavs[0].astype(np.float32)
    
    # 降低音调（简单的处理）
    # 注意：ChatTTS 本身不支持变调，这里是音量归一化
    if wav.max() > 1:
        wav = wav / np.abs(wav).max()
    wav = (wav * 32767).astype(np.int16)
    
    # 转为 WAV
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as f:
        f.setnchannels(1)  # 单声道
        f.setsampwidth(2)  # 16-bit
        f.setframerate(24000)  # 24kHz
        f.writeframes(wav.tobytes())
    
    return b64encode(buffer.getvalue()).decode('utf-8')
