#!/usr/bin/env python3
import urllib.request, json

API_KEY = "ai_xZY8Sz5nJuXAzWs1QDMyisYNKWJvgPaBX9Nz9thKUHXu1rIz"
BASE_URL = "https://aitoearn.ai/api/unified/mcp"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def mcp_call(name, args=None):
    payload = json.dumps({"jsonrpc":"2.0","method":"tools/call","params":{"name":name,"arguments":args or {}},"id":1}).encode("utf-8")
    req = urllib.request.Request(BASE_URL, data=payload, method="POST")
    req.add_header("x-api-key", API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    req.add_header("User-Agent", UA)
    with urllib.request.urlopen(req, timeout=25) as resp:
        raw = json.loads(resp.read())
        content = raw.get("result",{}).get("content",[])
        if content and content[0].get("type") == "text":
            text = content[0]["text"]
            try: return json.loads(text)
            except: return text
        return raw

print("=== YouTube 账号信息 ===")
r = mcp_call("getYouTubeChannelInfo", {})
print(str(r)[:300])

print("\n=== 已有素材 ===")
r = mcp_call("listMedia", {"pageNo":1,"pageSize":5})
print(str(r)[:400])

print("\n=== 已有草稿 ===")
r = mcp_call("listDrafts", {"pageNo":1,"pageSize":5})
print(str(r)[:400])

print("\n=== AI 创作定价 ===")
r = mcp_call("getDraftGenerationPricing")
if isinstance(r, dict):
    video = r.get("videoModels", [])
    print(f"视频模型: {[v.get('model') for v in video[:8]]}")
    img = r.get("imageModels", [])
    print(f"图片模型: {[i.get('model') for i in img[:5]]}")
    for v in video[:3]:
        print(f"  {v.get('model')}: {v.get('displayName')} - {v.get('maxDuration', 'N/A')}s max")
