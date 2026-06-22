# team-coordinator-status — 最新汇总

**更新时间**: 2026-06-22 19:00 (Asia/Shanghai)

---

## 整体状态: 🟢 健康

| 维度 | 状态 |
|------|------|
| Render 生产服务 | 🟢 v2.0.0, /api/health HTTP 200 |
| Git 同步 | 🟢 HEAD=origin/main=`95c7a5c` |
| team-deep-check | 🟡 16:00 报告缺失（本次 coordinator 运行 LLM 超时）；20:00 深检将覆盖 |
| 本次 coordinator | 🟡 LLM 超时（consecutiveErrors=1） |
| 核心闭环 | 🟢 7x24 自动运转 |

---

## 已知阻塞

- 🔴 aitoearn TikTok 粉丝不足（≥100），持续无法接单，需人工涨粉
- 🟡 本次 coordinator LLM 超时，下一次应自动恢复
- 🟡 企业微信回调 URL 验证（田太平人工操作）
- 🟡 memory 文件积累归档（建议处理）

---

*last updated: 2026-06-22 19:00 CST*