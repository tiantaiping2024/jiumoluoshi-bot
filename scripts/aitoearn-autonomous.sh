#!/bin/bash
# AiToEarn 7x24 Autonomous Earning Script
# 每次运行：侦察任务 → 选最优 → 接单 → 发布 → 提交

API_KEY="ai_xZY8Sz5nJuXAzWs1QDMyisYNKWJvgPaBX9Nz9thKUHXu1rIz"
BASE_URL="https://aitoearn.ai/api/unified/mcp"
LOG_DIR="/Users/tiantaiping/.openclaw/workspace/memory"
TIMESTAMP=$(date +%Y-%m-%d-%H)
LOGFILE="$LOG_DIR/aitoearn-run-$TIMESTAMP.md"

mkdir -p "$LOG_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOGFILE"
}

call_mcp() {
  local method="$1"
  local name="$2"
  local args="$3"
  curl -s "$BASE_URL" \
    -H "x-api-key: $API_KEY" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d "{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"$name\",\"arguments\":$args},\"id\":$$}" \
    --max-time 30
}

# ─── Step 1: Scout Tasks ───────────────────────────────────────
log "## 🚀 AiToEarn 自动赚钱任务 [$TIMESTAMP]"

PROFILE=$(call_mcp tools/call getMyProfile "{}")
USER_NAME=$(echo "$PROFILE" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)
log "**账户:** $USER_NAME"

BALANCE=$(call_mcp tools/call getMyBalance "{}")
AVAIL=$(echo "$BALANCE" | grep -o '"balance":[0-9]*' | cut -d':' -f2)
log "**当前余额:** \$$AVAIL USD"

# ─── Step 2: List Tasks ────────────────────────────────────────
log "### 📋 任务侦察中..."

TASKS=$(call_mcp tools/call listTaskMarket '{"pageNo":1,"pageSize":15}')
echo "$TASKS" > /tmp/aitoearn_tasks_$$.json

TOTAL=$(echo "$TASKS" | grep -o '"total":[0-9]*' | head -1 | cut -d':' -f2)
log "**市场任务总数:** $TOTAL"

# 解析任务列表，找最优任务
# 优先级：CPE任务 > 有奖励 > 名额充足 > 粉丝门槛低
log "### 🏆 任务评估"

# 找所有 active 且还有名额的任务
TASK_IDS=$(echo "$TASKS" | grep -o '"id":"[^"]*"' | head -20 | cut -d'"' -f4)

BEST_TASK=""
BEST_SCORE=0
BEST_REWARD=0

for tid in $TASK_IDS; do
  DETAIL=$(call_mcp tools/call getTaskDetail "{\"taskId\":\"$tid\"}")
  
  # 提取关键字段
  TITLE=$(echo "$DETAIL" | grep -o '"title":"[^"]*"' | head -1 | cut -d'"' -f4 | sed 's/\\//g')
  TYPE=$(echo "$DETAIL" | grep -o '"type":"[^"]*"' | head -1 | cut -d'"' -f4)
  REWARD=$(echo "$DETAIL" | grep -o '"reward":[0-9]*' | head -1 | cut -d':' -f2)
  CPE=$(echo "$DETAIL" | grep -o '"cpeReward":[0-9]*' | head -1 | cut -d':' -f2)
  MAX=$(echo "$DETAIL" | grep -o '"maxRecruits":[0-9]*' | head -1 | cut -d':' -f2)
  CUR=$(echo "$DETAIL" | grep -o '"currentRecruits":[0-9]*' | head -1 | cut -d':' -f2)
  FANS=$(echo "$DETAIL" | grep -o '"fansNum":[0-9]*' | head -1 | cut -d':' -f2)
  PLATFORMS=$(echo "$DETAIL" | grep -o '"accountTypes":\[[^]]*\]' | head -1)
  
  # 计算总分：奖励*10 + CPE/10 + (1/粉丝门槛)*100 + 名额空间*5
  FANS_SCORE=$( [ "$FANS" -eq 0 ] && echo 100 || echo $((100 / (FANS + 1))) )
  SLOT_SPACE=$((MAX - CUR))
  SCORE=$((REWARD * 10 + CPE / 10 + FANS_SCORE + SLOT_SPACE * 5))
  
  log "- **[$tid]** $TITLE | 类型:$TYPE | 基础奖励:\$$REWARD | CPE:\$$CPE | 名额:$CUR/$MAX | 粉丝门槛:$FANS | 平台:$PLATFORMS | 评分:$SCORE"
  
  if [ "$SCORE" -gt "$BEST_SCORE" ] && [ "$SLOT_SPACE" -gt 0 ]; then
    BEST_SCORE=$SCORE
    BEST_TASK=$tid
    BEST_TITLE="$TITLE"
    BEST_TYPE="$TYPE"
    BEST_REWARD=$REWARD
    BEST_CPE=$CPE
    BEST_PLATFORM=$(echo "$DETAIL" | grep -o '"accountTypes":\[[^]]*\]' | head -1)
  fi
done

log "### 🎯 选中任务: **$BEST_TASK** ($BEST_TITLE)"
log "   平台: $BEST_PLATFORM | 基础奖励: \$$BEST_REWARD | CPE: \$$BEST_CPE"

# ─── Step 3: Accept Task ────────────────────────────────────────
log "### ✅ 接取任务..."
ACCEPT_RESP=$(call_mcp tools/call acceptTask "{\"taskId\":\"$BEST_TASK\"}")
log "接单响应: $ACCEPT_RESP"

USER_TASK_ID=$(echo "$ACCEPT_RESP" | grep -o '"userTaskId":"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -z "$USER_TASK_ID" ]; then
  USER_TASK_ID=$(echo "$ACCEPT_RESP" | grep -o '"id":"[^"]*"' | head -3 | tail -1 | cut -d'"' -f4)
fi

if [ -z "$USER_TASK_ID" ]; then
  log "⚠️ 接单未返回 userTaskId，尝试从响应解析..."
  # 打印完整响应以便调试
  log "完整响应: $ACCEPT_RESP"
fi

if [ -n "$USER_TASK_ID" ]; then
  log "**userTaskId:** $USER_TASK_ID"
  
  # ─── Step 4: 尝试验证发布能力 ───────────────────────────────
  # 检查是否可以用已有素材发布
  log "### 📦 检查发布能力..."
  
  # 列出当前已有素材
  DRAFTS=$(call_mcp tools/call listDrafts '{"pageNo":1,"pageSize":5}')
  DRAFT_COUNT=$(echo "$DRAFTS" | grep -o '"total":[0-9]*' | head -1 | cut -d':' -f2)
  log "当前草稿数: $DRAFT_COUNT"
  
  MEDIA=$(call_mcp tools/call listMedia '{"pageNo":1,"pageSize":5}')
  MEDIA_TOTAL=$(echo "$MEDIA" | grep -o '"total":[0-9]*' | head -1 | cut -d':' -f2)
  log "当前素材数: $MEDIA_TOTAL"
  
  # ─── Step 5: 如果有素材，尝试发布并提交 ─────────────────────
  if [ "$DRAFT_COUNT" -gt 0 ] || [ "$MEDIA_TOTAL" -gt 0 ]; then
    log "✅ 检测到可用素材，尝试创建发布流程..."
    
    # 尝试创建发布
    # 注意：真实发布需要 accountId 和平台 OAuth，这里只是探测
    PLATFORMS_LIST=$(echo "$BEST_TASK" | grep -o '"accountTypes":\[[^]]*\]' | head -1)
    log "需要发布平台: $PLATFORMS_LIST"
    log "⚠️ 正式发布需要先在 AiToEarn Web 界面授权对应平台账号"
  else
    log "⚠️ 当前无素材可用"
    log "💡 建议：前往 https://aitoearn.ai 创建草稿/素材，或使用 AI 生成功能"
  fi
  
  # ─── Step 6: 提交任务（如果有 workLink） ────────────────────
  # 如果没有真实作品，诚实记录
  if [ -n "$USER_TASK_ID" ]; then
    log "### 📝 任务状态记录"
    log "**userTaskId:** $USER_TASK_ID 已存档，待补充作品后提交"
  fi
else
  log "❌ 接单失败或未获得 userTaskId，跳过提交"
fi

# ─── Step 7: Affiliate 扫描 ────────────────────────────────────
log "### 💰 Affiliate 推广链接检查..."
AFF_OVERVIEW=$(call_mcp tools/call getAffiliateOverview "{}")
log "返佣概览: $AFF_OVERVIEW"

AFF_LINK=$(call_mcp tools/call getAffiliateLink "{}")
log "推广链接: $AFF_LINK"

# ─── Summary ───────────────────────────────────────────────────
log "### 📊 本轮执行摘要"
log "- 时间: $TIMESTAMP"
log "- 最优任务: $BEST_TASK ($BEST_TITLE)"
log "- 平台: $BEST_PLATFORM"  
log "- 评分: $BEST_SCORE"
log "- 接单状态: $([ -n "$USER_TASK_ID" ] && echo "✅ 已接 (userTaskId: $USER_TASK_ID)" || echo "❌ 未接单")"
log "- 余额: $AVAIL USD"

log "---"
log "*此报告由 AiToEarn 自动赚钱引擎生成 | $(date)*"

# 清理临时文件
rm -f /tmp/aitoearn_tasks_$$.json
