# Team Deep Check — 2026-08-28 16:11 CST

## 1. Git 同步状态
- **分支**: main (本地 + origin/main)
- **最新提交**: `9589ac3` — docs: team-coordinator report 2026-08-28-10
- **工作区状态**: 干净（无 staged 变更）
- **未跟踪文件**:
  - `memory/aitoearn-run-2026-08-28-{11,12,13,14,15}.md` — 5 个 aitoearn 运行记录未提交
  - `memory/team-coordinator-2026-08-28-12.md` — 协作者报告未提交
  - `memory/team-deep-check-2026-08-28-12.md` — 上次深检报告未提交
- **结论**: Git 基本正常，有文件待提交

## 2. Render 生产健康
- **URL**: https://aitoearn.render.com/api/health
- **结果**: ❌ HEALTH_CHECK_FAILED (curl 超时或连接失败)
- **建议**: 检查 Render 服务是否在线，或服务域名/端口是否变更

## 3. aitoearn 扫描状态
- **scanner/status.json**: ❌ 未找到
- **本地 aitoearn 目录**: 不存在于 workspace
- **运行记录** (memory/aitoearn-run-2026-08-28-*.md):
  - 最近 5 次运行记录存在于 memory/ 目录
  - 最新: `aitoearn-run-2026-08-28-15.md` (15:22 CST)
- **结论**: aitoearn 项目目录不在预期位置，scanner 状态文件缺失

## 4. Cron Jobs 列表
- **job id**: `77493094-f094-4c1b-975f-855e2683312f`
- **name**: `team-deep-check`
- **enabled**: ✅ true
- **状态**: ⚠️ error
- **上次运行错误**:
  > Exec failed: find files named "aitoearn" in ~ -> show first 20 lines → list files in ~/ -> search "aito" in 2>/dev/null (exit 1)
- **上次 delivery**: ❌ not-delivered
- **下次运行**: `1787904000000` (时间戳，需转换)
- **结论**: job 持续报错，delivery 失败；scanner 路径问题需修复

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
- **结论**: weather 有记录（1752283500 ≈ 2026-07-11 CST，过期）；email/calendar 从未检查

## 6. 汇总与待办

| 项目 | 状态 | 备注 |
|------|------|------|
| Git 同步 | ⚠️ | 多个 memory 文件未提交 |
| Render 健康 | ❌ | 连接失败，需排查 |
| aitoearn scanner | ❌ | 目录/状态文件缺失 |
| team-deep-check cron | ❌ | job 报错，delivery 失败 |
| heartbeat state | ⚠️ | 检查项几乎未初始化 |

### 建议行动
1. 检查 Render 服务状态（可能是 free tier 休眠或域名变更）
2. 确认 aitoearn 项目实际路径，修复 scanner 状态文件位置
3. 修复 `team-deep-check` cron job 的 exec 命令（find aitoearn 路径）
4. 提交 memory/*.md 待跟踪文件

---
*深检时间: 2026-08-28 16:11 CST*
