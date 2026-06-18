# MEMORY.md - 鸠摩罗什Bot 长期记忆

## 身份与项目

- **项目**: 鸠摩罗什Bot (jiumoluoshi-bot)
- **生产地址**: `https://jiumoluoshi-bot.onrender.com`
- **版本**: v2.0.0
- **技术栈**: Python FastAPI + OpenClaw Agent + DeepSeek API

## 团队自动化架构

### Cron Jobs
- **`team-deep-check`** (每4小时): 深检报告，调度: `0 0,4,8,12,16,20 * * *`，sessionTarget=isolated
- **`team-coordinator-hourly`** (每小时): 每小时状态报告，运行于**两处**: 本地机器 + Render worker/CI (team-coordinator@jiumoluoshi.bot)，两地各自提交导致 Git 分叉 ⚠️
  - 本地: `tiantaiping2024@users.noreply.github.com` 推送 local commits
  - Render CI: `team-coordinator@jiumoluoshi.bot` 推送 origin commits
  - **已合并** (2026-06-14 12:00): `90718307` = origin/main

### 报告存储
- `memory/team-deep-check-YYYY-MM-DD-HH.md` — 4小时深检报告（workspace memory/）
- `memory/team-coordinator-YYYY-MM-DD-HH.md` — 每小时协调员报告
- `jiumoluoshi-bot/memory/team-coordinator-YYYY-MM-DD-HH.md` — 同上（repo内副本）
- `jiumoluoshi-bot/memory/team-coordinator-status.md` — 最新汇总状态

### 闭环链路
开发 → Git push → Render 自动部署 → health check → 运营闭环

## 关键联系人

- **田太平**: 项目负责人，负责企业微信回调验证等需要人工确认的事项

## 已知问题

### P3: 企业微信回调 URL 验证（持续悬而未决）
- **问题**: 回调 URL 已更新为 Render 生产地址，需田太平在企业微信应用后台"发送测试"确认消息能到达
- **状态**: 持续多日未解决，不影响核心闭环

### team-coordinator-hourly 状态（双实例运行）
- **双实例确认**: `team-coordinator-hourly` 在本地机器和 Render worker 两处各自运行，导致 Git 分叉
  - 本地 commit author: `tiantaiping2024@users.noreply.github.com`
  - Render CI commit author: `team-coordinator@jiumoluoshi.bot`
- **分叉处理**: 2026-06-14 12:00 合并 origin/main 到本地 HEAD，解决了 team-coordinator-status.md 冲突 ✅

## 稳定运行记录

- Render 生产服务持续健康（v2.0.0）
- Git 同步率: 100%（`0e772e4` = origin/main，workspace；`5e90cba` = origin/main，jiumoluoshi-bot）
- 闭环自 2026-06-06 以来无 P0/P1/P2 阻塞

## 教训

- **2026-06-12 08:00**: team-deep-check 因 AI 过载失败，之后连续正常
- cron job 删除后若无记录难以追溯，应在 workspace 内记录所有 job 配置
- 外部触发器（如 Render webhook）可作为 cron 的备份触发机制

---

*最后更新: 2026-06-19 04:04 (Asia/Shanghai)*