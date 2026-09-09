# Team Deep Check Report
**时间:** 2026-09-09 08:02 CST (Asia/Shanghai)
**UTC:** 2026-09-09 00:02 UTC

---

## 1. Git 同步状态

- **当前分支:** `main`
- **本地 HEAD:** `c75a53c` — chore: coordinator report 2026-09-09 06:00 CST
- **origin/main 最新:** 未能确认（git fetch 超时，无返回）
- **状态:** ⚠️ fetch 超时，无法确认远程是否有新提交

---

## 2. Render 生产健康

- **端点:** `https://aitoearn.onrender.com/api/health`
- **结果:** ❌ 超时（curl exit 28）
- **状态:** 🔴 不可达或响应超时

---

## 3. AiToEarn 扫描状态

- **最近扫描:** `2026-09-09 04:43 CST`
- **扫描结果:** 发现 3 个任务
  - TikTok promotion AITOEARN Platform — 🔴 失败：粉丝不足（门槛≥100）
- **接单结果:** ❌ 本轮未能接取任何任务
- **状态:** ⚠️ 运行正常但账号条件未达标

---

## 4. Cron Jobs

| Job | 状态 | 上次运行 | 上次状态 |
|-----|------|---------|---------|
| team-deep-check | ✅ 启用 | 1788897850103 (≈2026-09-09 07:44 CST) | ❌ error |

- **nextRunAtMs:** 1788912000000 (约 2026-09-09 18:40 CST)

---

## 5. Heartbeat State

```json
{
  "lastChecks": {
    "email": null,
    "calendar": null,
    "weather": 1752283500
  },
  "coordinator": {
    "lastReport": 1752266500
  }
}
```

- **weather 上次检查:** 1752283500（需换算）
- **coordinator 上次报告:** 1752266500

---

## 汇总

| 检查项 | 状态 |
|--------|------|
| Git 同步 | ⚠️ fetch 超时，无法确认 |
| Render 健康 | 🔴 超时不可达 |
| AiToEarn 扫描 | ⚠️ 运行中但账号条件未达标 |
| Cron Jobs | ✅ team-deep-check 存在（上次 error） |
| Heartbeat | ⚠️ email/calendar 从未检查 |

**建议:**
1. 确认 Render 服务是否在线或冷启动中
2. 检查 Git 网络连接是否稳定
3. 考虑为 email/calendar 设置心跳检查
