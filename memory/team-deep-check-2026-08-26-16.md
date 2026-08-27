# team-deep-check Report
**时间:** 2026-08-26 16:03 CST (UTC 08:03)
**执行:** isolated agent | session: 77493094-f094-4c1b-975f-855e2683312f

---

## 1. Git 同步状态

| 项目 | 状态 |
|------|------|
| 当前分支 | main |
| 本地最新提交 | 7b28c22 — docs: team-coordinator report (2026-08-26 12:49 CST) |
| origin/main 最新 | 7b28c22 — 与本地一致，无落后 |
| 远程分支 | origin/main |
| 同步状态 | ✅ 同步正常，无待推送/拉取 commits |

---

## 2. Render 生产健康检查

| 项目 | 状态 |
|------|------|
| 域名 | https://aitoearn-api.onrender.com |
| /api/health 响应 | HTTP 404 (路由不存在) |
| /health 响应 | HTTP 404 (路由不存在) |
| 服务可达性 | ⚠️ 服务在线(有响应)，但健康检查端点未配置 |
| 结论 | Render 服务运行中，健康检查路由需配置 |

---

## 3. aitoearn 扫描状态

| 项目 | 状态 |
|------|------|
| ~/.aitoearn 目录 | ❌ 目录不存在 |
| scan_state 目录 | ❌ SCAN_STATE_DIR_MISSING |
| latest.json | ❌ NO_LATEST_SCAN |
| 结论 | aitoearn 扫描状态文件缺失，需确认扫描任务是否正常运行 |

---

## 4. Cron Jobs

| Job ID | Name | 状态 | 上次运行 | 上次状态 |
|--------|------|------|----------|----------|
| 77493094-f094-4c1b-975f-855e2683312f | team-deep-check | enabled | 1787716800012 | error ⚠️ |

**详情:**
- Next run: 1787731200000 (需换算)
- 上次运行状态: **error** — 需进一步排查

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

| 项目 | 状态 |
|------|------|
| email | 从未检查 |
| calendar | 从未检查 |
| weather | 上次检查: 1752283500 (需换算) |

---

## 汇总 & 待办

### ✅ 正常
- Git 与 origin/main 同步，无差异

### ⚠️ 需关注
1. **Render API** — `/api/health` 和 `/health` 路由均 404，健康检查端点需配置
2. **aitoearn 扫描状态** — ~/.aitoearn 目录不存在，扫描任务可能未运行或路径配置错误
3. **Cron team-deep-check** — 上次运行状态为 error，需排查
4. **Heartbeat** — email/calendar 从未检查，weather 距今可能已久

### 📝 下次深检跟进
- [ ] 确认 aitoearn 扫描脚本实际路径和运行状态
- [ ] 在 Render 侧添加 `/api/health` 端点或使用已有端点
- [ ] 排查 team-deep-check 上次 error 的原因
- [ ] 建议用户配置 heartbeat email/calendar 检查

---

*Report generated: 2026-08-26 16:03 CST*
