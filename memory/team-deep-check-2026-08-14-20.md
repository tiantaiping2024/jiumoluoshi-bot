# Team Deep Check — 2026-08-14 20:05 CST

## 1. Git 同步状态
- **本地 HEAD**: `765ff26` (2026-08-14 19:17 CST)
- **远程状态**: `git fetch` 无输出，`git log HEAD..origin/main` 无输出
- **结论**: ✅ 本地与远程 main 分支已同步，无待拉取 commits

## 2. Render 生产健康
- **检查命令**: `curl -s --max-time 8 https://aitoearn.com/api/health`
- **响应**: 无输出（超时或连接失败）
- **历史背景**: 此前已有多次 Render 404 / 休眠报告
- **结论**: ⚠️ Render 生产端可能仍处于休眠或故障状态

## 3. aitoearn 扫描状态
- **进程**: 无 aitoearn 相关 node 进程运行中
- **目录**: `~/.aitoearn/` 不存在
- **scan-state.json**: 不存在
- **结论**: 🔴 aitoearn 扫描任务未运行，目录/配置缺失

## 4. Cron Jobs
| Job | Enabled | Last Run | Status |
|-----|---------|----------|--------|
| team-deep-check | ✅ | 1786694400014 | ⚠️ error |

- 仅注册一个 cron job（team-deep-check 自检）
- 上次运行状态为 `error`，需关注

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
- 上次 weather check: Jul 12 09:45（距今约33天前）
- email / calendar 从未检查过
- **结论**: ⚠️ Heartbeat 检查机制近乎停摆

## 6. 汇总

| 项目 | 状态 |
|------|------|
| Git 同步 | ✅ 正常 |
| Render 健康 | ⚠️ 休眠/故障 |
| aitoearn 扫描 | 🔴 未运行 |
| Cron (team-deep-check) | ⚠️ 上次 error |
| Heartbeat 检查 | ⚠️ 停摆（33天无weather，email/calendar从未运行）|

---
*深检时间: 2026-08-14 20:05 CST (UTC 12:05)*
