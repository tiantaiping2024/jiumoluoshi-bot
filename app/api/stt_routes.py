"""
Deepgram STT 语音识别
前端通过 Web Audio API + MediaRecorder 录制完整音频
结束时将整个录音转为 base64 发送
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
    """使用 Deepgram 转录音频（完整录音模式）"""
    try:
        body = await request.body()
        
        # 解析 JSON
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
        
        print(f"[STT] Received {len(audio_data)} bytes")
        
        # 保存为 webm 文件
        debug_dir = "/tmp/stt_debug"
        os.makedirs(debug_dir, exist_ok=True)
        import time
        ts = int(time.time() * 1000)
        webm_file = f"{debug_dir}/audio_{ts}.webm"
        with open(webm_file, "wb") as f:
            f.write(audio_data)
        
        # 转换: webm → 16kHz mono linear16 PCM WAV
        wav_file = f"{debug_dir}/audio_{ts}.wav"
        result = subprocess.run([
            'ffmpeg', '-y', '-i', webm_file,
            '-ar', '16000', '-ac', '1', '-acodec', 'pcm_s16le',
            '-f', 'wav', '-hide_banner', wav_file
        ], capture_output=True, timeout=30)
        
        os.unlink(webm_file)
        
        if result.returncode != 0:
            print(f"[STT] ffmpeg error: {result.stderr.decode()[:300]}")
            return {"transcript": "", "error": f"ffmpeg: {result.stderr.decode()[:150]}"}
        
        # 读取 WAV 数据
        with open(wav_file, 'rb') as f:
            wav_data = f.read()
        os.unlink(wav_file)
        
        print(f"[STT] Converted to {len(wav_data)} bytes PCM WAV")
        
        # 发送 L16 PCM 到 Deepgram
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
            return {"transcript": "", "error": f"Deepgram {response.status_code}: {response.text[:100]}"}
        
        result_data = response.json()
        
        # 提取 transcript
        transcript = ""
        try:
            for channel in result_data.get("results", {}).get("channels", []):
                for alternative in channel.get("alternatives", []):
                    if alternative.get("transcript"):
                        transcript += alternative["transcript"] + " "
        except Exception as e:
            print(f"[STT] Parse error: {e}")
        
        print(f"[STT] Transcript: '{transcript.strip()}'")
        return {"transcript": transcript.strip()}
        
    except requests.exceptions.Timeout:
        return {"transcript": "", "error": "Deepgram request timeout"}
    except Exception as e:
        print(f"[STT] Error: {e}")
        return {"transcript": "", "error": str(e)}