# Team Deep Check — 2026-08-29 00:08 CST

## 1. Git 同步状态

- **HEAD commit**: `706b947` (2026-08-28 18:24 CST)
- **origin/main**: `706b947` (已确认 fetch 成功)
- **同步率**: ✅ 100% (本地 = origin/main)
- **最近活动**: docs sync team reports and aitoearn runs

## 2. Render 生产健康

- **健康检查**: `curl https://aitoearn.com/api/health` → 无输出 (exit code 0)
  - ⚠️ 注意：本次检查的是 `aitoearn.com/api/health`（aitoearn 平台），而非鸠摩罗什Bot 的 `jiumoluoshi-bot.onrender.com`
  - MEMORY 记录：aitoearn.ai 平台 health OK（最近多次）
- **已知状态**:
  - `jiumoluoshi-bot.onrender.com` — 历史上 Free tier 休眠导致 404（非真实宕机）
  - `aitoearn.onrender.com` — 历史上下线/超时
  - `aitoearn.ai` — 平台级健康（最近多次）
- **状态**: ⚠️ 待确认鸠摩罗什Bot Render 实际健康（需 main session 检查 jiumoluoshi-bot.onrender.com）

## 3. aitoearn 扫描状态

- **scan_state.json**: ❌ 不存在 (`~/.aitoearn/scan_state.json`)
- **.scan_lock**: ❌ 不存在
- **~/.aitoearn/ 目录**: ❌ 不存在
- **结论**: aitoearn 扫描状态文件缺失，可能是平台下线或目录被清理
- **历史 MEMORY**: aitoearn.ai 平台最近健康，但 onrender.com 版本的 aitoearn-api 历史上多次下线
- **状态**: ⚠️ aitoearn 扫描状态不可读

## 4. Cron Jobs 列表

| Job | Enabled | Schedule | lastRunStatus | lastError |
|-----|---------|----------|---------------|-----------|
| `team-deep-check` | ✅ true | cron `0 0,4,8,12,16,20 * * *` | 🔴 error | null |

- **nextRunAtMs**: 1787932800000 (≈ 2026-08-29 04:00 CST)
- **lastRunAtMs**: 1787919051245 (≈ 2026-08-28 20:04 CST)
- **lastRunStatus**: error（本次触发但 isolated session 执行出错）
- **lastDeliveryStatus**: unknown
- **lastFailureNotificationDeliveryStatus**: unknown
- **⚠️ 注意**: 只显示 team-deep-check job，team-coordinator-hourly 不在当前 isolated session 视野内（属本地机器另一套 cron 表）

## 5. Heartbeat State

```json
{
  "lastChecks": {
    "email": null,
    "calendar": null,
    "weather": 1752283500
  }
}
```

- **email**: null（从未设置）
- **calendar**: null（从未设置）
- **weather**: 1752283500（≈ 2026-07-11 15:25 CST，约 **49天前** ⚠️）
- **结论**: heartbeat state 严重过期，weather 检查已 49 天未更新

## 6. 汇总

### ✅ 正常项
- Git 100% 同步
- team-deep-check cron job 注册表存在，调度正常
- 团队技术闭环基本可用

### ⚠️ 需关注
- **aitoearn 扫描状态**: `~/.aitoearn/` 目录缺失，扫描状态不可读；aitoearn.ai 平台健康但 onrender.com 版本历史上下线
- **Render 生产**: 未直接检查 `jiumoluoshi-bot.onrender.com/api/health`，Bot 实际状态待 main session 确认
- **heartbeat-state.json**: weather 检查 49 天未更新，email/calendar 从未配置
- **team-deep-check lastRunStatus=error**: isolated session 执行出错，但 cron 调度正常

### 🔴 长期阻塞（持续）
- **TikTok 涨粉阻塞**: 粉丝 < 100，任务门槛 ≥ 100，持续 ~110天+
- **aitoearn 重复接单 bug**: `aitoearn-accepted-tasks.json` 有大量重复 taskId 记录

---

*深检完成: 2026-08-29 00:08 CST*
*执行者: team-deep-check isolated agent*
