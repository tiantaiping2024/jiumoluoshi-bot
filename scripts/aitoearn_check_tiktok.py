#!/usr/bin/env python3
import urllib.request, json, yaml

KEY_FILE = "/Users/tiantaiping/.openclaw/workspace/scripts/aitoearn_key.txt"
API_KEY = open(KEY_FILE).read().strip()
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
            if text.startswith("list:"):
                return yaml.safe_load(text)
            try: return json.loads(text)
            except: return text
        return raw

# 尝试获取 TikTok 账号信息
tools = [
    ("getChannelAccountInfo", {"platform": "tiktok", "username": "TheMindfulEast"}),
    ("getChannelAccountInfo", {"platform": "tiktok", "accountId": "themindfuleast"}),
    ("getAccountInfo", {"platform": "tiktok"}),
    ("getChannelAnalytics", {"platform": "tiktok"}),
    ("getMyChannelInfo", {}),
    ("listMyChannels", {}),
    ("getTiktokInfo", {}),
]

print("=== 探测 TikTok 账号信息工具 ===")
for name, args in tools:
    r = mcp_call(name, args)
    if "_error" not in r:
        print(f"\n✅ {name}({args}):")
        print(str(r)[:400])
    else:
        print(f"❌ {name}: {str(r)[:80]}")
