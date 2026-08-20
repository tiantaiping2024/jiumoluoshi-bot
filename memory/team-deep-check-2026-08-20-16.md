# Team Deep Check Report
**时间:** 2026-08-20 16:00 CST (周四)
**UTC:** 2026-08-20 08:00 UTC

---

## 1. Git 同步状态 ✅

```
6a82817 coord: 11:16 CST report - Render ~45h down, TikTok ~110d blocked
a49666a coord: 17:13 CST report - Render ~27h down, TikTok ~110d, coordinator recovered
d98df5f MEMORY: 12:13 CST - Render ~20h down, TikTok ~109d, coordinator recovered
d839297 coord: 12:13 CST report - Render 双服务下线 ~20h, TikTok ~109d blocked
6b02f4a coord: 16:03 CST report - 🔴 Render 双服务下线, TikTok ~108d blocked
```
- 最新 commit: `6a82817` (11:16 CST)
- Git 同步正常，无落后

---

## 2. Render 生产健康 🔴

- **端点:** `https://aitoearn.onrender.com/api/health`
- **结果:** ❌ CURL_FAILED (请求超时或服务不可达)
- **历史记录:** Render 自 8/18 起持续下线约 45h，尚未恢复

---

## 3. aitoearn 扫描状态 ⚠️

- 日志目录 `/Users/tiantaiping/.aitoearn/logs/` 不存在或为空
- 无法确认扫描任务运行状态

---

## 4. Cron Jobs 列表

| Job ID | 名称 | 状态 | 上次运行 | 上次结果 |
|--------|------|------|----------|----------|
| 77493094-f094-4c1b-975f-855e2683312f | team-deep-check | ✅ 启用 | 1787198400010 | ❌ error |

- 仅 1 个 cron job 注册运行
- 上次运行状态: `error`

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
- weather 最后检查: 1752283500 (需转换确认时间)

---

## 汇总

| 项目 | 状态 |
|------|------|
| Git 同步 | ✅ 正常 |
| Render 健康 | 🔴 离线 (~45h+) |
| aitoearn 扫描 | ⚠️ 无法确认 |
| Cron Jobs | ⚠️ 上次 error |
| Heartbeat | ⚠️ 仅 weather 有记录 |

**建议:** Render 服务持续下线需关注；aitoearn 日志目录需确认是否正确配置。
