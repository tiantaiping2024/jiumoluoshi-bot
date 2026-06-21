#!/usr/bin/env python3
"""
AiToEarn 7x24 Autonomous Earning Script v2
策略升级：当首选任务不满足粉丝门槛时，自动降级找更低门槛任务
"""
import urllib.request, json, yaml, os, sys
from datetime import datetime

KEY_FILE = "/Users/tiantaiping/.openclaw/workspace/scripts/aitoearn_key.txt"
API_KEY = open(KEY_FILE).read().strip()
BASE_URL = "https://aitoearn.ai/api/unified/mcp"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

LOG_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
os.makedirs(LOG_DIR, exist_ok=True)
TIMESTAMP = datetime.now().strftime("%Y-%m-%d-%H")
LOGFILE = f"{LOG_DIR}/aitoearn-run-{TIMESTAMP}.md"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOGFILE, "a") as f:
        f.write(line + "\n")

def mcp_call(name, args=None):
    payload = json.dumps({
        "jsonrpc": "2.0", "method": "tools/call",
        "params": {"name": name, "arguments": args or {}}, "id": 1
    }).encode("utf-8")
    req = urllib.request.Request(BASE_URL, data=payload, method="POST")
    req.add_header("x-api-key", API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    req.add_header("User-Agent", UA)
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            raw = json.loads(resp.read())
            content = raw.get("result", {}).get("content", [])
            if content and content[0].get("type") == "text":
                text = content[0]["text"]
                if text.startswith("list:"):
                    return yaml.safe_load(text)
                try: return json.loads(text)
                except: return text
            return raw
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}: {e.read().decode()[:200]}"}

log("## 🚀 AiToEarn 自动赚钱任务 v2")
log(f"**时间:** {TIMESTAMP}")

# 1. 账户
profile = mcp_call("getMyProfile")
name = profile.get("name", "?") if isinstance(profile, dict) else "?"
log(f"**账户:** {name}")

balance = mcp_call("getMyBalance")
if isinstance(balance, dict):
    log(f"**余额:** ${balance.get('balance', 0)} USD | **总收益:** ${balance.get('totalIncome', 0)} USD")

# 2. 扫描所有任务
log("### 📋 任务市场扫描...")
tasks_raw = mcp_call("listTaskMarket", {"pageNo": 1, "pageSize": 50})
if isinstance(tasks_raw, dict) and "_error" in tasks_raw:
    log(f"❌ MCP失败: {tasks_raw['_error']}")
    sys.exit(1)

tasks = tasks_raw.get("list", []) if isinstance(tasks_raw, dict) else []
log(f"**总数:** {tasks_raw.get('total', '?')} | **本页:** {len(tasks)}")

# 3. 按平台分组 + 可接性分析
platform_names = {
    "youtube": "YouTube", "instagram": "Instagram",
    "twitter": "X/Twitter", "tiktok": "TikTok",
    "xhs": "小红书", "threads": "Threads",
    "bilibili": "B站", "douyin": "抖音"
}

log("### 📊 各平台任务状态")
available_tasks = []  # 有名额的任务
for t in tasks:
    cur, maxr = t.get("currentRecruits", 0), t.get("maxRecruits", 0)
    slots = maxr - cur
    if slots <= 0:
        continue
    fans = t.get("acceptRules", {}).get("fansNum", 999) if isinstance(t.get("acceptRules"), dict) else 999
    plat = t.get("accountTypes", [])
    reward = t.get("reward", 0)
    cpe = t.get("cpeReward", 0)
    score = cpe // 10 + reward * 5 + slots * 5 + max(0, 50 - fans)
    t["_slots"] = slots
    t["_fans"] = fans
    t["_score"] = score
    available_tasks.append(t)

    plat_str = ",".join([platform_names.get(p, p) for p in plat])
    status_icon = "🔴" if fans > 0 else "🟢"
    log(f"  {status_icon} [{plat_str}] slots={slots}/{maxr} fans≥{fans} reward=${reward}+CPE${cpe} | {t.get('title','')[:45]}")

available_tasks.sort(key=lambda x: x["_score"], reverse=True)

# 4. 尝试接任务 — 逐个尝试直到成功
ACCEPTED_TASKS = []
FAILED_REASONS = []

log("### 🎯 尝试接取任务（从最高分到最低）")
for t in available_tasks:
    tid = t.get("_id")
    title = t.get("title", "")[:50]
    fans = t["_fans"]
    plat = t.get("accountTypes", [])
    reward = t.get("reward", 0)
    cpe = t.get("cpeReward", 0)
    score = t["_score"]

    log(f"\n尝试: {title}")
    log(f"  platform={plat} fans≥{fans} reward=${reward}+CPE${cpe} score={score}")

    r = mcp_call("acceptTask", {"taskId": tid})
    resp_str = str(r)

    if "userTaskId" in resp_str or ("success" in resp_str.lower() and "error" not in resp_str.lower()):
        log(f"  ✅ 接单成功! 响应: {resp_str[:200]}")
        ACCEPTED_TASKS.append(t)
        break  # 先接一个，成功了就不继续了
    else:
        reason = "粉丝不足" if "follower" in resp_str.lower() else ("满员" if "full" in resp_str.lower() else resp_str[20:100])
        log(f"  ❌ 失败: {reason}")
        FAILED_REASONS.append({"id": tid, "title": title, "reason": reason, "fans": fans})

# 5. 结果记录
log("\n### 📝 接单结果")
if ACCEPTED_TASKS:
    for t in ACCEPTED_TASKS:
        log(f"✅ **接单成功!**")
        log(f"   任务: {t.get('title','')[:60]}")
        log(f"   平台: {t.get('accountTypes')}")
        log(f"   奖励: ${t.get('reward',0)} + CPE${t.get('cpeReward',0)}")
        log(f"   下一步: 前往 https://aitoearn.ai 完成任务并提交")
        # 保存到待提交文件
        PENDING_FILE = f"{LOG_DIR}/aitoearn-accepted-tasks.json"
        pending = []
        if os.path.exists(PENDING_FILE):
            pending = json.load(open(PENDING_FILE))
        pending.append({
            "timestamp": TIMESTAMP,
            "taskId": t.get("_id"),
            "title": t.get("title"),
            "platforms": t.get("accountTypes"),
            "reward": t.get("reward", 0),
            "cpeReward": t.get("cpeReward", 0),
            "status": "pending"
        })
        json.dump(pending, open(PENDING_FILE, "w"), ensure_ascii=False, indent=2)
        log(f"   已存档至 {PENDING_FILE}")
else:
    log("❌ 本轮未能接取任何任务")
    if FAILED_REASONS:
        log("失败原因汇总:")
        for fr in FAILED_REASONS:
            log(f"  - {fr['title'][:40]}: {fr['reason']} (粉丝门槛≥{fr['fans']})")
    log("💡 建议:")
    log("  1. 前往 https://aitoearn.ai 手动查看是否有新增任务")
    log("  2. 检查账号平台授权是否生效")
    log("  3. 关注粉丝数量，达标后下次自动接单")

# 6. Affiliate 检查
log("\n### 💰 Affiliate 推广链接")
aff_link = mcp_call("getAffiliateLink")
if isinstance(aff_link, dict):
    inner = aff_link.get("result", {})
    if isinstance(inner, dict):
        code = inner.get("inviteCode", "")
        link = inner.get("inviteLink", "")
        log(f"邀请码: {code}")
        log(f"推广链接: {link}")
        log(f"💡 分享给朋友，他们完成任务你可获返佣！")

log("\n*由 AiToEarn 自动赚钱引擎 v2 生成*")
log("---")
