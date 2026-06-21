#!/usr/bin/env python3
import urllib.request, urllib.error, json, sys

API_KEY = "ai_xZY8Sz5nJuXAzWs1QDMyisYNKWJvgPaBX9Nz9thKUHXu1rIz"
BASE_URL = "https://aitoearn.ai/api/unified/mcp"

def mcp_call(name, args=None):
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": name, "arguments": args or {}},
        "id": 1
    }).encode("utf-8")
    req = urllib.request.Request(BASE_URL, data=payload, method="POST")
    req.add_header("x-api-key", API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}: {e.read().decode()}"}

print("=== 1. Profile ===")
r = mcp_call("getMyProfile")
print(r)

print("\n=== 2. Balance ===")
r = mcp_call("getMyBalance")
print(r)

print("\n=== 3. Task Market (top 12) ===")
r = mcp_call("listTaskMarket", {"pageNo": 1, "pageSize": 12})
if "_error" in r:
    print("ERROR:", r["_error"])
    sys.exit(1)

content_text = r["result"]["content"][0]["text"]
tasks = json.loads(content_text)
print(f"Total: {tasks['total']}")
for t in tasks["list"]:
    tid = t.get("_id","")
    title = t.get("title","")
    typ = t.get("type","")
    reward = t.get("reward",0)
    cpe = t.get("cpeReward",0)
    cur = t.get("currentRecruits",0)
    maxr = t.get("maxRecruits",0)
    fans = t.get("acceptRules",{}).get("fansNum",0)
    platforms = t.get("accountTypes",[])
    slots = maxr - cur
    print(f"  [{typ}] {title[:50]} | reward=${reward} cpe=${cpe} | {cur}/{maxr} slots | fans>={fans} | {platforms}")
    print(f"    -> _id: {tid}")

# Pick best task
best = None
best_score = -1
for t in tasks["list"]:
    tid = t["_id"]
    reward = t.get("reward", 0)
    cpe = t.get("cpeReward", 0)
    fans = t.get("acceptRules", {}).get("fansNum", 0)
    slots = t.get("maxRecruits", 0) - t.get("currentRecruits", 0)
    score = reward * 10 + cpe // 10 + (100 // (fans + 1)) + slots * 5
    if slots > 0 and score > best_score:
        best_score = score
        best = t

if best:
    print(f"\n=== 4. Best Task ===")
    print(f"ID: {best['_id']}")
    print(f"Title: {best['title']}")
    print(f"Type: {best['type']}")
    print(f"Platforms: {best['accountTypes']}")
    print(f"Reward: ${best.get('reward',0)} | CPE: ${best.get('cpeReward',0)}")
    print(f"Slots: {best['currentRecruits']}/{best['maxRecruits']}")
    print(f"Score: {best_score}")

    print("\n=== 5. Accept Task ===")
    r = mcp_call("acceptTask", {"taskId": best["_id"]})
    print("acceptTask result:", r)
    if "_error" not in r and "result" in r:
        inner = r["result"]["content"][0]["text"]
        print("acceptTask inner:", json.loads(inner) if inner.startswith("{") else inner)

print("\n=== 6. Affiliate Overview ===")
r = mcp_call("getAffiliateOverview")
print(r)

print("\n=== 7. Affiliate Link ===")
r = mcp_call("getAffiliateLink")
if "_error" not in r and "result" in r:
    inner = r["result"]["content"][0]["text"]
    data = json.loads(inner) if inner.startswith("{") else inner
    print(data)
    if isinstance(data, dict):
        print(f"Invite Code: {data.get('inviteCode')}")
        print(f"Invite Link: {data.get('inviteLink')}")
