# Team Deep Check — 2026-08-01 20:07 CST

## 1. Git 同步状态
- **状态**: ✅ 已同步
- **本地最新 commit**: `1145102` — "chore: coordinator 19:00 CST 2026-08-01 - aitoearn-run log archive, status update"
- **git fetch**: 无输出，origin/main 无领先提交

## 2. Render 生产健康
- **状态**: ⚠️ 超时/不可达
- **Endpoint**: `https://aitoearn.onrender.com/api/health`
- **结果**: curl 超时（10s），exit code 28 — 可能是 Render 空闲实例冷启动或网络问题

## 3. aitoearn 扫描状态
- **状态**: ❌ 目录不存在
- **检查路径**: `/Users/tiantaiping/.aitoearn/`
- **结果**: 目录未找到，scan_state.json 不存在

## 4. Cron Jobs 列表
| Job ID | 名称 | 状态 | 下次运行 |
|--------|------|------|----------|
| `77493094-f094-4c1b-975f-855e2683312f` | team-deep-check | enabled | error (lastRunStatus) |

- 当前仅 1 个 job（就是本任务本身）
- **lastRunStatus**: error — 需要关注

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
- **上次 weather check**: 1752283500 (约 2026-07-11?) — 较旧
- **email/calendar**: 从未检查过

## 汇总

| 项目 | 状态 |
|------|------|
| Git 同步 | ✅ 正常 |
| Render 健康 | ⚠️ 超时，注意冷启动 |
| aitoearn 扫描 | ❌ 目录缺失，需排查 |
| Cron jobs | ⚠️ lastRunStatus=error |
| Heartbeat | ⚠️ email/calendar 从未检查 |

**建议行动**:
1. 确认 aitoearn 安装路径或配置
2. 排查 team-deep-check cron 上次 error 原因
3. Render 超时可能是空闲实例，可尝试重新触发一次
4. 考虑启用 email/calendar heartbeat 检查
