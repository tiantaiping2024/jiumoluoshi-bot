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

tasks_raw = mcp_call("listTaskMarket", {"pageNo":1,"pageSize":50})
tasks = tasks_raw.get("list",[]) if isinstance(tasks_raw,dict) else []
total = tasks_raw.get("total",0) if isinstance(tasks_raw,dict) else 0

print(f"市场任务总数: {total}，本页 {len(tasks)} 条\n")

platform_names = {
    "youtube": "YouTube",
    "instagram": "Instagram",
    "twitter": "X (Twitter)",
    "tiktok": "TikTok",
    "xhs": "小红书",
    "threads": "Threads",
    "bilibili": "B站",
    "douyin": "抖音",
    "wxGzh": "微信公众号",
    "kwai": "快手",
    "linkedin": "LinkedIn",
    "facebook": "Facebook",
    "pinterest": "Pinterest",
}

print("=" * 70)
print("📋 各平台任务状态一览")
print("=" * 70)

for plat_key, plat_name in platform_names.items():
    plat_tasks = [t for t in tasks if plat_key in t.get("accountTypes", [])]
    if not plat_tasks:
        continue
    print(f"\n🔷 {plat_name} — {len(plat_tasks)} 个任务")
    for t in plat_tasks:
        tid = t.get("_id","")
        title = t.get("title","")[:55]
        typ = t.get("type","")
        reward = t.get("reward",0)
        cpe = t.get("cpeReward",0)
        fans = t.get("acceptRules",{}).get("fansNum",0) if isinstance(t.get("acceptRules"),dict) else 0
        cur, maxr = t.get("currentRecruits",0), t.get("maxRecruits",0)
        slots = maxr - cur
        status = "✅" if slots > 0 else "❌ SOLD OUT"
        print(f"  {status} [{typ}] {title}")
        print(f"      奖励: ${reward} + CPE${cpe} | 名额: {cur}/{maxr} | 粉丝门槛: ≥{fans}")
        print(f"      id={tid}")

print("\n" + "=" * 70)
print("🎯 可接任务（有名额）优先尝试")
print("=" * 70)

available = [t for t in tasks if t.get("maxRecruits",0) - t.get("currentRecruits",0) > 0]
available.sort(key=lambda x: x.get("cpeReward",0) + x.get("reward",0)*5, reverse=True)

for t in available[:10]:
    plat = t.get("accountTypes",[])
    fans = t.get("acceptRules",{}).get("fansNum",0) if isinstance(t.get("acceptRules"),dict) else 0
    reward = t.get("reward",0)
    cpe = t.get("cpeReward",0)
    cur, maxr = t.get("currentRecruits",0), t.get("maxRecruits",0)
    print(f"\n⭐ {t.get('title','')[:60]}")
    print(f"   平台: {plat} | reward=${reward} + CPE${cpe}")
    print(f"   名额: {cur}/{maxr} | 粉丝门槛: ≥{fans}")
    print(f"   id={t.get('_id')}")

# 尝试接受最优可接任务
if available:
    best = available[0]
    best_id = best.get("_id")
    print(f"\n{'='*70}")
    print(f"🚀 尝试接取最优任务: {best.get('title','')[:50]}")
    print(f"   platform={best.get('accountTypes')} id={best_id}")
    r = mcp_call("acceptTask", {"taskId": best_id})
    print(f"响应: {r}")
PYEOF