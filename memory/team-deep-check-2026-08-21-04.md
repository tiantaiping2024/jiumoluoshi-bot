# Team Deep Check · 2026-08-21 04:10 CST

## 检查时间
- CST: 2026-08-21 04:10
- UTC: 2026-08-20 20:10

---

## 1. Git 同步

| 项目 | 状态 | 详情 |
|------|------|------|
| HEAD | ✅ 正常 | `f2ef88a` — cleanup: remove stale aitoearn-run logs (2026-08-18/19) |
| 最新提交 | 🟡 3天前 | 2026-08-18，距今约 3 天 |
| 未推送 | ❓ | 本次仅 fetch，未深入检查 local branches |

**结论**: ✅ main 与 origin/main 同步，无落后。

---

## 2. Render 生产健康

| 项目 | 状态 | 详情 |
|------|------|------|
| `/api/health` | ⚠️ 空响应 | `curl` exit=0，无输出，可能是 204 No Content 或空 200 |
| 响应特征 | ⚠️ 待确认 | 需要再次抓取完整响应头确认状态 |

**历史背景**（from run history）:
- 2026-08-20 16:03 报告：Render ~48h 下线
- 2026-08-18 16:00 报告：Render 404 offline
- 持续离线约 3 天以上

**结论**: 🔴 疑似持续离线，curl 返回空（可能是 Render Free 实例已终止或未绑定域名）

---

## 3. aitoearn 扫描状态

| 项目 | 状态 | 详情 |
|------|------|------|
| 目录 `~/.aitoearn/` | ❌ 不存在 | `cd:1: no such file or directory` |
| `scan_state.json` | ❌ 不存在 | 无扫描状态文件 |
| `aitoearn` 工作目录 | ❌ 缺失 | 扫描系统从未初始化或已移除 |

**结论**: 🔴 aitoearn 扫描系统未部署/未初始化，依赖 Render 上线后才有意义。

---

## 4. Cron Jobs

| 项目 | 状态 |
|------|------|
| Job 数量 | 1 (仅 team-deep-check) |
| 上次运行 | ⚠️ error: `AbortError: agent run aborted` (2026-08-20 23:03 CST，约 3.5h 前) |
| 下次运行 | 2026-08-21 06:00 CST |

**最近 5 次运行结果**:
| 时间 (CST) | 状态 | 错误 |
|------------|------|------|
| 08-20 23:03 | error | AbortError: agent run aborted |
| 08-20 21:36 | error | AbortError: agent run aborted |
| 08-20 20:16 | error | Feishu delivery requires target |
| 08-20 18:56 | error | FailoverError: overloaded |
| 08-20 17:36 | error | LLM timeout |

**错误模式分析**:
- 主要错误: `AbortError: agent run aborted` (约 80% of runs) — isolated session 被强制中止
- 次要: `Feishu delivery requires target` — 报告无法推送至 Feishu（channel 配置缺失 to 参数）
- 偶发: LLM overload/timeout

**结论**: ⚠️ team-deep-check 反复报错，但 job 本身正常调度（下次 06:00 CST）。孤立 session 中止问题需调查。

---

## 5. Heartbeat State

| 检查项 | 上次执行 | 状态 |
|--------|----------|------|
| email | 从未 | ❌ |
| calendar | 从未 | ❌ |
| weather | ~3h 前 (1752283500 ≈ 2025-07) | 🟡 数据过期 |

`heartbeat-state.json` 内容:
```json
{
  "lastChecks": {
    "email": null,
    "calendar": null,
    "weather": 1752283500
  }
}
```

**结论**: ⚠️ email/calendar 从未配置检查；weather 时间戳为 2025-07（过期约 1 年）。

---

## 汇总

| 检查项 | 状态 | 备注 |
|--------|------|------|
| **Git** | ✅ | 与 origin 同步，HEAD `f2ef88a` |
| **Render** | 🔴 | 持续离线 3 天+，`/api/health` 空响应 |
| **aitoearn** | 🔴 | 目录不存在，扫描系统未初始化 |
| **Cron Jobs** | ⚠️ | 仅 1 job，反复 AbortError，需排查 isolated session 中止原因 |
| **Heartbeat** | ⚠️ | email/calendar 从未检查，weather 数据过期 1 年 |

---

## 待办建议

1. **Render**: 确认实例状态，如已终止需重新部署
2. **aitoearn**: 确认扫描系统部署方式及工作目录位置
3. **Cron AbortError**: 调查 isolated session 中止原因（可能是超时/内存限制）
4. **Feishu delivery**: 修复 channel delivery target 配置，使报告能正常推送
5. **Heartbeat**: 配置 email/calendar 周期性检查

---

*报告生成: 2026-08-21 04:10 CST · team-deep-check isolated agent*
