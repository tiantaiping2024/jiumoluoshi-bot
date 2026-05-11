"""
阿里云百炼 STT 语音识别 - 使用 Paraformer 实时识别
支持 webm 格式输入（前端 MediaRecorder 默认格式）
"""
import os
import base64
import json
import tempfile
import subprocess
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

stt_router = APIRouter()


@stt_router.post("/stream")
async def stream_stt():
    """阿里云百炼流式语音识别（已弃用）"""
    return JSONResponse({"status": "deprecated"})


@stt_router.post("/transcribe")
async def transcribe_audio(request: Request):
    """使用阿里云百炼 Paraformer 转录音频（支持本地文件）"""
    try:
        body = await request.body()
        
        # 尝试解析 JSON
        try:
            data = json.loads(body)
            audio_base64 = data.get("audio", "")
        except:
            audio_base64 = body.decode("utf-8", errors="ignore")
        
        if not audio_base64:
            raise HTTPException(status_code=400, detail="No audio provided")
        
        # 解码音频
        try:
            if "," in audio_base64:
                audio_base64 = audio_base64.split(",")[1]
            audio_data = base64.b64decode(audio_base64)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid audio data: {e}")
        
        if not DASHSCOPE_API_KEY:
            return {"transcript": "", "error": "DASHSCOPE_API_KEY not configured"}
        
        # 使用阿里云百炼实时识别 API
        import dashscope
        from dashscope.audio.asr import Recognition
        
        dashscope.api_key = DASHSCOPE_API_KEY
        
        # 将 webm/ogg 转换为 wav（16kHz 单声道），ffmpeg 已在 Docker 中安装
        try:
            # 先保存原始音频
            with tempfile.NamedTemporaryFile(delete=False, suffix='.webm', mode='wb') as f:
                f.write(audio_data)
                webm_file = f.name
            # 转换为目标 wav 文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav', mode='wb') as f:
                wav_file = f.name
            subprocess.run([
                'ffmpeg', '-y', '-i', webm_file,
                '-ar', '16000', '-ac', '1', '-acodec', 'pcm_s16le',
                wav_file
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            return {"transcript": "", "error": f"Audio conversion failed: {e.stderr.decode() if e.stderr else str(e)}"}
        finally:
            try:
                os.unlink(webm_file)
            except:
                pass

        try:
            # 调用 Paraformer 实时识别
            recognition = Recognition(
                model='paraformer-realtime-v2',
                format='wav',
                sample_rate=16000,
                language_hints=['zh', 'en'],
                callback=None
            )
            result = recognition.call(wav_file)
            
            if result.status_code != 200:
                return {"transcript": "", "error": result.message}
            
            # 提取文本
            sentences = result.get_sentence()
            if sentences:
                transcript = "".join([s.text for s in sentences])
                return {"transcript": transcript}
            
            return {"transcript": ""}
            
        finally:
            try:
                os.unlink(wav_file)
            except:
                pass
                
    except Exception as e:
        print(f"STT error: {e}")
        return {"transcript": "", "error": str(e)}