"""
Deepgram STT 语音识别
前端 MediaRecorder 采集的 webm/opus 音频流转为 base64 发送至此
转换为 16kHz mono linear16 PCM WAV 后发送给 Deepgram
"""
import os
import base64
import json
import tempfile
import subprocess
import requests
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

stt_router = APIRouter()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
DEEPGRAM_URL = "https://api.deepgram.com/v1/listen"


@stt_router.post("/transcribe")
async def transcribe_audio(request: Request):
    """使用 Deepgram 转录音频（webm/opus → 16kHz PCM WAV）"""
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
        
        if not DEEPGRAM_API_KEY:
            return {"transcript": "", "error": "DEEPGRAM_API_KEY not configured"}
        
        # 转换格式：webm/opus → 16kHz mono linear16 PCM WAV
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.webm', mode='wb') as f:
                f.write(audio_data)
                webm_file = f.name
            
            wav_file = tempfile.mktemp(suffix='.wav')
            result = subprocess.run([
                'ffmpeg', '-y', '-i', webm_file,
                '-ar', '16000', '-ac', '1', '-acodec', 'pcm_s16le',
                '-f', 'wav', wav_file
            ], capture_output=True, timeout=30)
            
            if result.returncode != 0:
                return {"transcript": "", "error": f"ffmpeg error: {result.stderr.decode()}"}
            
            # 读取转换后的 WAV 数据
            with open(wav_file, 'rb') as f:
                wav_data = f.read()
                
        finally:
            for f in [webm_file, wav_file]:
                try:
                    os.unlink(f)
                except:
                    pass
        
        # 发送给 Deepgram
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/l16",
        }
        params = {
            "model": "nova-2",
            "language": "zh-CN",
            "sample_rate": "16000",
            "smart_format": "true",
            "punctuate": "true",
        }
        
        response = requests.post(
            DEEPGRAM_URL,
            headers=headers,
            params=params,
            data=wav_data,
            timeout=30
        )
        
        if response.status_code != 200:
            return {"transcript": "", "error": f"Deepgram error: {response.status_code} {response.text}"}
        
        result = response.json()
        
        # 提取 transcript
        transcript = ""
        try:
            for channel in result.get("results", {}).get("channels", []):
                for alternative in channel.get("alternatives", []):
                    if alternative.get("transcript"):
                        transcript += alternative["transcript"] + " "
        except Exception as e:
            return {"transcript": "", "error": f"Parse error: {e}"}
        
        transcript = transcript.strip()
        return {"transcript": transcript}
        
    except subprocess.TimeoutExpired:
        return {"transcript": "", "error": "Audio conversion timeout"}
    except requests.exceptions.Timeout:
        return {"transcript": "", "error": "Deepgram request timeout"}
    except Exception as e:
        print(f"STT error: {e}")
        return {"transcript": "", "error": str(e)}