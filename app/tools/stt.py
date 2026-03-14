"""
阿里云百炼 STT 语音识别模块 - 使用 Qwen3-ASR-Flash
"""
import os
import base64
import requests


DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
STT_MODEL = "qwen3-asr-flash-2026-02-10"


def transcribe_audio(audio_data: bytes, language: str = "zh-CN") -> str:
    """使用阿里云百炼 ASR 转录音频"""
    if not DASHSCOPE_API_KEY:
        return ""
    
    try:
        import dashscope
        from dashscope import MultiModalConversation
        
        dashscope.api_key = DASHSCOPE_API_KEY
        
        # 保存临时文件
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
            f.write(audio_data)
            temp_file = f.name
        
        try:
            # 调用 ASR
            resp = MultiModalConversation.call(
                model=STT_MODEL,
                messages=[{
                    'role': 'user',
                    'content': [{'audio': f'file://{temp_file}'}]
                }],
                stream=False
            )
            
            if resp.get("status_code") != 200:
                print(f"ASR error: {resp.get('message')}")
                return ""
            
            # 提取文本
            output = resp.get("output", {})
            choices = output.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                content = message.get("content", [])
                if content:
                    return content[0].get("text", "")
            
            return ""
            
        finally:
            # 删除临时文件
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"ASR 转录错误: {e}")
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
