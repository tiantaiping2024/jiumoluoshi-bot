# Team Deep Check Report
**时间**: 2026-08-23 00:07 CST (UTC: 2026-08-22 16:07)
**执行者**: team-deep-check isolated agent

---

## 1. Git 同步状态

```
HEAD -> main, origin/main 同步
最近提交 (2026-08-21 16:46 CST):
  79f3591 docs: add team-coordinator report
  26f133f chore: archive aitoearn-run logs
  2f2ef88a cleanup: remove stale aitoearn-run logs
  928a792 coord: 17:03 CST report - Render ~48h down, TikTok ~110d blocked
  ... (更多见 git log)
```
**状态**: ✅ 正常，无本地未推送提交

---

## 2. Render 生产健康检查

```
curl https://aitoearn.onrender.com/api/health
结果: RENDER_UNREACHABLE (超时/连接失败)
```
**状态**: 🔴 Render 服务下线持续中 (从 2026-08-19 起已约 3.5 天)

---

## 3. aitoearn 扫描状态

- 无独立进程运行 (本机未部署守护进程)
- 今日 run logs (2026-08-22): 15h / 17h / 19h / 21h / 22h 各一条
- 说明 aitoearn 依赖 cron 触发而非持续运行

---

## 4. Cron Jobs

| ID | 名称 | 状态 | 上次运行 | 上次状态 |
|---|---|---|---|---|
| `77493094-...` | team-deep-check | ✅ enabled | 2026-08-22 23:42 CST | ⚠️ error (lastRunStatus: error) |

**注**: 仅有 1 个 cron job，team-deep-check 本身运行结果为 error，但本轮执行正常完成

---

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
**状态**: ⚠️ email/calendar 从未检查过；weather 检查时间戳 = 1752283500 (约 2026-07-12)，已过期

---

## 6. 汇总

| 检查项 | 状态 | 备注 |
|---|---|---|
| Git 同步 | ✅ 正常 | origin/main 同步 |
| Render 健康 | 🔴 下线 | 持续约 3.5 天 |
| aitoearn 扫描 | ⚪ 被动 | cron 触发，无守护进程 |
| Cron Jobs | ⚠️ 1个error | team-deep-check 上次 error |
| Heartbeat | ⚠️ 未激活 | email/calendar 从未检查 |

---

*报告生成: 2026-08-23 00:07 CST*
