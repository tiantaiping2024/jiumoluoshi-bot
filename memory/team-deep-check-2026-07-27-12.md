# Team Deep Check — 2026-07-27 12:00 CST

## 1. Git 同步状态
- **状态**: ✅ 正常
- **最新 commit**: `7ed2cfc` — "chore: coordinator 11:00 CST 2026-07-27 + deep-check cron 第8次失踪需重建"
- **分支**: HEAD (无待推送/拉取变更)
- **最近10条日志**: 2026-07-26 10:00 起有多次 coordinator 提交，11:00 已执行

## 2. Render 生产健康
- **状态**: ❌ 不可达
- **检查**: `curl https://aitoearn.onrender.com/api/health` → RENDER_UNREACHABLE
- **建议**: Render 免费实例可能已休眠，需冷启动或检查实例状态

## 3. aitoearn 扫描状态
- **状态**: ⚠️ 扫描状态文件不存在
- **目录**: `/Users/tiantaiping/.aitoearn/` 未找到 scan_state.json
- **进程**: 未发现运行中的 aitoearn 相关进程
- **建议**: 确认 aitoearn 是否部署/配置正确，或处于未启动状态

## 4. Cron Jobs
| Job ID | Name | 状态 | 下次运行 |
|--------|------|------|----------|
| 77493094-f094-4c1b-975f-855e2683312f | team-deep-check | ⚠️ error (上次执行报错) | 2026-07-27 18:00 CST |

- **问题**: team-deep-check 上次运行状态为 `error`，需要排查重建

## 5. Heartbeat State
```json
{
  "lastChecks": {
    "email": null,
    "calendar": null,
    "weather": 1752283500  // 约 2026-07-26 21:05 CST
  }
}
```
- **问题**: email/calendar 从未检查过，weather 已超 15 小时未更新

## 汇总

| 项目 | 状态 | 备注 |
|------|------|------|
| Git | ✅ | 同步正常 |
| Render | ❌ | 不可达（休眠或实例问题） |
| aitoearn | ⚠️ | 无状态文件，无进程运行 |
| Cron (deep-check) | ⚠️ | 上次 error，需重建 |
| Heartbeat | ⚠️ | 多项检查长期未执行 |

**需要关注**: Render 实例健康 + aitoearn 实际部署状态 + team-deep-check cron 报错原因
