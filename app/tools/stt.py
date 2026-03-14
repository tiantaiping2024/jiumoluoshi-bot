"""
阿里云 DashScope STT 语音识别模块 - 使用 Qwen3-ASR-Flash
"""
import os
import json
import base64
import requests


DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
STT_MODEL = "qwen3-asr-flash-2026-02-10"


def transcribe_audio(audio_data: bytes, language: str = "zh-CN") -> str:
    """使用阿里云 DashScope ASR 转录音频"""
    if not DASHSCOPE_API_KEY:
        return ""
    
    try:
        url = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"
        
        headers = {
            "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # 将音频转为 base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        payload = {
            "model": STT_MODEL,
            "input": {
                "file_urls": [f"data:audio/webm;base64,{audio_base64}"]
            },
            "parameters": {
                "language_hints": [language]
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            # 检查是否有 transcription_url
            if "output" in result and "transcription_url" in result.get("output", {}):
                # 需要轮询获取结果
                transcription_url = result["output"]["transcription_url"]
                return poll_transcription_result(transcription_url, headers)
        
        print(f"ASR response: {response.status_code} - {response.text}")
        return ""
    except Exception as e:
        print(f"ASR 转录错误: {e}")
        return ""


def poll_transcription_result(url: str, headers: dict, max_retries: int = 10) -> str:
    """轮询获取转录结果"""
    import time
    
    for i in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                result = response.json()
                status = result.get("output", {}).get("task_status", "")
                
                if status == "SUCCEEDED":
                    # 获取转录文本
                    transcripts = result.get("output", {}).get("transcripts", [])
                    if transcripts:
                        return transcripts[0].get("text", "")
                elif status == "FAILED":
                    return ""
            
            time.sleep(1)
        except Exception as e:
            print(f"轮询错误: {e}")
            time.sleep(1)
    
    return ""


def transcribe_base64(audio_base64: str, language: str = "zh-CN") -> str:
    """从 Base64 转录音频"""
    if not audio_base64:
        return ""
    
    try:
        # 处理 data URL 格式
        if "," in audio_base64:
            audio_base64 = audio_base64.split(",")[1]
        
        audio_data = base64.b64decode(audio_base64)
        return transcribe_audio(audio_data, language)
    except Exception as e:
        print(f"Base64 转录错误: {e}")
        return ""


async def transcribe_audio_async(audio_data: bytes, language: str = "zh-CN") -> str:
    """异步封装"""
    import asyncio
    return await asyncio.to_thread(transcribe_audio, audio_data, language)


async def transcribe_base64_async(audio_base64: str, language: str = "zh-CN") -> str:
    """异步封装"""
    import asyncio
    return await asyncio.to_thread(transcribe_base64, audio_base64, language)
