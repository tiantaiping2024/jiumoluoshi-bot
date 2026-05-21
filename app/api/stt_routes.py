"""
Deepgram STT 语音识别
前端 MediaRecorder 采集的 webm/opus 音频流转为 base64 发送至此
尝试 ogg/opus 格式（Deepgram 原生支持）
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
    """使用 Deepgram 转录音频"""
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
        
        # 保存调试文件
        debug_dir = "/tmp/stt_debug"
        os.makedirs(debug_dir, exist_ok=True)
        import time
        ts = int(time.time() * 1000)
        debug_file = f"{debug_dir}/audio_{ts}.webm"
        with open(debug_file, "wb") as f:
            f.write(audio_data)
        print(f"[STT] Saved {len(audio_data)} bytes to {debug_file}")
        
        # 方法1：尝试直接用 webm 发送（Deepgram 官方支持）
        for content_type, ext in [
            ("audio/webm", "webm"),
            ("audio/ogg", "ogg"),
            ("audio/opus", "opus"),
        ]:
            print(f"[STT] Trying {content_type}...")
            params = {
                "model": "nova-2",
                "language": "zh-CN",
                "smart_format": "true",
                "punctuate": "true",
            }
            headers = {
                "Authorization": f"Token {DEEPGRAM_API_KEY}",
                "Content-Type": content_type,
            }
            
            response = requests.post(
                DEEPGRAM_URL,
                headers=headers,
                params=params,
                data=audio_data,
                timeout=30
            )
            
            print(f"[STT] {content_type} → {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                transcript = ""
                try:
                    for channel in result.get("results", {}).get("channels", []):
                        for alternative in channel.get("alternatives", []):
                            if alternative.get("transcript"):
                                transcript += alternative["transcript"] + " "
                except Exception as e:
                    print(f"[STT] Parse error: {e}")
                print(f"[STT] Transcript: '{transcript.strip()}'")
                return {"transcript": transcript.strip()}
            else:
                print(f"[STT] {content_type} failed: {response.text[:200]}")
        
        # 方法2：尝试 ffmpeg 转换
        print("[STT] Trying ffmpeg conversion...")
        try:
            wav_file = f"{debug_dir}/audio_{ts}.wav"
            result = subprocess.run([
                'ffmpeg', '-y', '-i', debug_file,
                '-ar', '16000', '-ac', '1', '-acodec', 'pcm_s16le',
                '-f', 'wav', wav_file
            ], capture_output=True, timeout=30)
            
            if result.returncode == 0:
                with open(wav_file, 'rb') as f:
                    wav_data = f.read()
                print(f"[STT] ffmpeg converted to {len(wav_data)} bytes WAV")
                
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
                
                if response.status_code == 200:
                    result = response.json()
                    transcript = ""
                    try:
                        for channel in result.get("results", {}).get("channels", []):
                            for alternative in channel.get("alternatives", []):
                                if alternative.get("transcript"):
                                    transcript += alternative["transcript"] + " "
                    except Exception as e:
                        pass
                    return {"transcript": transcript.strip()}
                else:
                    print(f"[STT] WAV failed: {response.text[:200]}")
            else:
                print(f"[STT] ffmpeg error: {result.stderr.decode()[:200]}")
        finally:
            for f in [debug_file, wav_file]:
                try:
                    os.unlink(f)
                except:
                    pass
        
        return {"transcript": "", "error": "All STT methods failed"}
        
    except requests.exceptions.Timeout:
        return {"transcript": "", "error": "Deepgram request timeout"}
    except Exception as e:
        print(f"[STT] Error: {e}")
        return {"transcript": "", "error": str(e)}