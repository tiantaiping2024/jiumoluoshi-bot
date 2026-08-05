# Team Deep Check — 2026-08-05 08:03 CST

## 1. Git 同步状态
- **workspace**: synced, latest commit `39b13ce` (coordinator 05:02 CST - status report, exec EAGAIN 自愈, aitoearn 宕机 ~9天)
- **aitoearn**: ❌ 目录不存在 (`~/.aitoearn` 或 `~/aitoearn` 均未找到)，无法检查

## 2. Render 生产健康
- **aitoearn.onrender.com**: ❌ UNREACHABLE — curl 超时/连接失败
- 备注：aitoearn.ai 持续宕机已 ~9天

## 3. aitoearn 扫描状态
- ❌ 无法检查 — 本地代码仓库不存在
- 推测：可能宕机前已停止运行

## 4. Cron Jobs
| Name | Enabled | Next Run (UTC) | Last Status |
|------|---------|----------------|-------------|
| team-deep-check | ✅ | 2026-08-05 08:00 CST | ⚠️ error |

> nextRunAtMs: 1785888000000 → 2026-08-05 12:00 UTC (今晚8点 CST)

## 5. Heartbeat State
```json
{
  "lastChecks": {
    "email": null,
    "calendar": null,
       "weather": 1752283500  ← 较旧(≈2025-07)
  }
}
```

## 6. 综合摘要

| 系统 | 状态 | 备注 |
|------|------|------|
| workspace git | ✅ 正常 | 最新commit 08-05 05:02 |
| aitoearn repo | ❌ 缺失 | 目录不存在 |
| Render 健康 | ❌ 离线 | aitoearn.onrender.com 不通 |
| aitoearn 扫描 | ❌ 不可用 | 无代码仓库 |
| Cron jobs | ⚠️ 1个job, last error | team-deep-check |
| Heartbeat | ⚠️ email/calendar 从未检查 | weather数据陈旧 |

---
*报告生成: 2026-08-05 08:03 CST (UTC+8)*
