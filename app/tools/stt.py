"""
语音识别模块 - 优先 Deepgram，备选阿里云百炼
"""
import os
import base64
import requests


DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
STT_MODEL = "qwen3-asr-flash-2026-02-10"


def transcribe_deepgram(audio_data: bytes, language: str = "zh-CN") -> str:
    """使用 Deepgram 转录"""
    if not DEEPGRAM_API_KEY:
        return None
    
    try:
        # 检测音频格式
        content_type = "audio/webm" if audio_data[:4] == b'\x1aE' else "audio/wav"
        
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": content_type
        }
        
        params = {
            "punctuate": "true",
            "language": language,
            "model": "nova-2"
        }
        
        response = requests.post(
            "https://api.deepgram.com/v1/listen",
            headers=headers,
            params=params,
            data=audio_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("results", {}).get("channels"):
                return result["results"]["channels"][0]["alternatives"][0]["transcript"]
        
        return None
    except Exception as e:
        print(f"Deepgram 转录错误: {e}")
        return None


def transcribe_aliyun(audio_data: bytes, language: str = "zh-CN") -> str:
    """使用阿里云百炼 ASR 转录"""
    if not DASHSCOPE_API_KEY:
        return None
    
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
            resp = MultiModalConversation.call(
                model=STT_MODEL,
                messages=[{
                    'role': 'user',
                    'content': [{'audio': f'file://{temp_file}'}]
                }],
                stream=False
            )
            
            if resp.get("status_code") != 200:
                return None
            
            output = resp.get("output", {})
            choices = output.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                content = message.get("content", [])
                if content:
                    return content[0].get("text", "")
            
            return None
            
        finally:
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"阿里云 ASR 转录错误: {e}")
        return None


def transcribe_audio(audio_data: bytes, language: str = "zh-CN") -> str:
    """转录音频 - 优先 Deepgram，备选阿里云"""
    # 优先用 Deepgram
    if DEEPGRAM_API_KEY:
        result = transcribe_deepgram(audio_data, language)
        if result:
            print(f"使用 Deepgram 转录: {result}")
            return result
    
    # 备选阿里云
    if DASHSCOPE_API_KEY:
        result = transcribe_aliyun(audio_data, language)
        if result:
            print(f"使用阿里云转录: {result}")
            return result
    
    return ""


def transcribe_base64(audio_base64: str, language: str = "zh-CN") -> str:
    """从 Base64 转录音频"""
    if not audio_base64:
        return ""
    
    try:
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
