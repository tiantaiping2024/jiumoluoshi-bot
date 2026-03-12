"""
ChatTTS 语音合成模块
支持抑扬顿挫、情感停顿、对话语音
"""
import io
import torch
import ChatTTS
import numpy as np
from base64 import b64encode


# 全局模型实例
_chat_tts = None
_torch_dtype = None


def get_chat_tts():
    """获取 ChatTTS 模型实例"""
    global _chat_tts, _torch_dtype
    
    if _chat_tts is None:
        # 加载模型
        _chat_tts = ChatTTS.InferProcess()
        
        # 优化：使用较轻量的推理
        _chat_tts.load(compile=True, source="custom")
        
    return _chat_tts


def synthesize_speech(text: str, speed: float = 0.9) -> bytes:
    """
    合成语音，返回 MP3 音频数据
    
    Args:
        text: 要转换的文本
        speed: 语速，0.8-1.2 之间，较慢更像高僧讲话
    
    Returns:
        MP3 音频数据
    """
    chat = get_chat_tts()
    
    # 准备文本
    texts = [text]
    
    # 生成参数
    # temperature: 温度，越高越有创造性
    # top_P: 采样参数
    # top_K: K值采样
    params_infer_code = {
        'temperature': 0.3,
        'top_P': 0.7,
        'top_K': 20,
    }
    
    # 语速控制
    params_refine_text = {
        'prompt': f'[speed={speed}]',  # 控制语速，值越小越慢
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
    合成语音，返回 WAV 格式 Base64（更高质量）
    """
    import wave
    
    chat = get_chat_tts()
    texts = [text]
    
    params_infer_code = {
        'temperature': 0.3,
        'top_P': 0.7,
        'top_K': 20,
    }
    
    params_refine_text = {
        'prompt': '[speed=0.9]',
    }
    
    wavs = chat.infer(
        texts,
        params_refine_text=params_refine_text,
        params_infer_code=params_infer_code,
    )
    
    wav = wavs[0].astype(np.float32)
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
