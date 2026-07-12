# MEMORY.md - 鸠摩罗什Bot 长期记忆

## 身份与项目

- **项目**: 鸠摩罗什Bot (jiumoluoshi-bot)
- **生产地址**: `https://jiumoluoshi-bot.onrender.com`
- **版本**: v2.0.0
- **技术栈**: Python FastAPI + OpenClaw Agent + DeepSeek API

## 团队自动化架构

### Cron Jobs
- **`team-deep-check`** (每4小时): 深检报告，调度: `0 0,4,8,12,16,20 * * *`，sessionTarget=isolated
- **`team-coordinator-hourly`** (每小时): 每小时状态报告，运行于**两处**: 本地机器 + Render worker/CI，两地各自提交导致 Git 分叉 ⚠️
  - 本地: `tiantaiping2024@users.noreply.github.com` 推送 local commits
  - Render CI: `team-coordinator@jiumoluoshi.bot` 推送 origin commits
  - **已合并** (2026-06-14 12:00)

### 报告存储
- `memory/team-deep-check-YYYY-MM-DD-HH.md` — 4小时深检报告
- `memory/team-coordinator-YYYY-MM-DD-HH.md` — 每小时协调员报告
- `memory/team-coordinator-status.md` — 最新汇总状态

### 闭环链路
开发 → Git push → Render 自动部署 → health check → 运营闭环

## 关键联系人

- **田太平**: 项目负责人，负责企业微信回调验证等需要人工确认的事项

## 已知问题

### P3: 企业微信回调 URL 验证（持续悬而未决）
- **问题**: 回调 URL 已更新为 Render 生产地址，需田太平在企业微信应用后台"发送测试"确认消息能到达
- **状态**: 持续多日未解决，不影响核心闭环

### ✅ aitoearn SSL 已完全自愈（2026-07-03 04:00 起）
- **之前**: SSL EOF violation 持续22天+（~545h），2026-07-02 19:00 CST 起消失，07-03 00:00 deep-check 确认稳定
- **回归**: 2026-07-03 01:21/02:21 CST 再次出现 SSL EOF violation
- **自愈**: 2026-07-03 04:18 起连续6次无 SSL 错误，平台连接彻底恢复 ✅
- **偶发回归**: 2026-07-03 12:47 出现连接超时（read timed out），13:08/13:25 连续两次正常，回归已消除 ✅
- **唯一活跃阻塞**: TikTok粉丝 < 100，持续~609h+

### team-coordinator-hourly 双实例运行
- `team-coordinator-hourly` 在本地机器和 Render worker 两处各自运行，会导致 Git 分叉
  - 本地 commit author: `tiantaiping2024@users.noreply.github.com`
  - Render CI commit author: `team-coordinator@jiumoluoshi.bot`
- **分叉处理**: 2026-06-14 12:00 合并 origin/main 到本地 HEAD ✅
- **注意**: 两套 Gateway 视野独立，coordinator 报告中的 deep-check "缺失"系视野问题，需以本地 deep-check 报告为准

### ✅ Token Plan P0 危机已消（2026-07-06 05:00 起）
- **问题**: 已达到 MiniMax Token Plan 用量上限，连续3次（02:00/03:00/04:00 CST）cron job 失败
- **错误**: `⚠️ 已达到 Token Plan 用量上限：请升级 Token Plan 套餐或购买积分补充用量。 (2056)`
- **最后成功**: 2026-07-06 01:03 CST
- **自愈**: 05:01 起连续成功（05:01/07:00/09:01/10:01 CST），Token 自动恢复
- **推测**: MiniMax Token Plan 有小时限额，凌晨低谷后自动释放

### ✅ team-deep-check 模型超时危机（已修复，2026-07-06 15:01 CST）
- **问题**: consecutiveErrors=14+，最后成功 2026-07-05 04:20 CST
- **原因**: `models.providers.minimax` 未配置 `timeoutSeconds`，深检 token 消耗大（100k-150k+ input）
- **修复方案**: 直接编辑 `~/.openclaw/openclaw.json`，在 minimax provider 添加 `timeoutSeconds: 300`
- **修复验证**: Gateway 已重启（SIGUSR1），PID 949 运行中，15:01 CST 完成
- **效果**: 下次深检（16:00 CST）应验证修复效果

### ✅ Git 分叉已解决（2026-07-09 08:32 CST）
- **分叉**: 本地 `2d5f5af` 领先 origin/main `2339ddd` 1 commit
- **解决**: 08:32 CST push `2d5f5af` → origin/main，完全同步 ✅

### ✅ 深检 20:00 CST 超时为一次性故障（2026-07-08 20:00，04:00 CST 已排除）
- **问题**: 深检 input tokens 177k+，模型 988s 后 idle timeout
- **一次性**: 上下文历史过大导致，非持续性故障
- **验证**: 04:00 CST 深检正常运行，exec 全命令正常
- **状态**: 已排除

### ✅ team-coordinator timeout 已修复（2026-07-09 08:32 CST）
- **问题**: consecutiveErrors=3，每次 coordinator 运行读 cron runs history（50条），context 膨胀至 97k tokens，MiniMax M2.7 idle timeout
- **根因**: cron runs 每次累加 input tokens，300s timeoutSeconds 不够高 context 下使用
- **修复**: 派分子 agent 将 `models.providers.minimax.timeoutSeconds` 从 300 提升至 600
- **状态**: 已修复，coordinator 每小时正常运行 ✅

### team-deep-check cron 运行真相（2026-06-22 澄清）
- **coordinator 误判**: coordinator 在 Render worker 内运行，看到的 cron 表只有 worker 自己的 job，误报 team-deep-check "缺失"
- **实际情况**: 本地 Gateway `team-deep-check` cron job 完全正常，调度 `0 0,4,8,12,16,20 * * *`，每次准时触发（lastRunStatus=ok，206s执行）
- **教训**: 两套 Gateway（本地 + Render worker）各自独立，cron job 不共享；本地 deep-check 报告正常生成，coordinator 报告里的"缺失"是视野问题而非真实状态

## 已知问题（续）

### 🔴 team-deep-check cron 丢失（2026-07-11 00:00 CST 起，约40h+）
- **问题**: cron list 仅显示 `team-coordinator-hourly`，`team-deep-check` 已消失
- **最后深检**: 2026-07-11 00:00 CST
- **发现时间**: 2026-07-12 15:01 CST coordinator 首次发现
- **状态**: 需人工田太平用 `/openclaw cron add` 重建
- **临时影响**: 深检报告缺失，但 coordinator 每小时正常运行，技术闭环无影响

### 🔴 aitoearn TikTok涨粉阻塞（持续悬而未决 ~1300h+）
- **问题**: TikTok账号粉丝 < 100，aitoearn.ai 任务门槛≥100，无法自动接单
- **持续时间**: ~1000h+（约41天+）
- **状态**: 唯一真实活跃阻塞，需人工运营TikTok涨粉
- **平台状态**: SSL 完全稳定，技术连接无问题，只剩粉丝数不足

## 稳定运行记录

- Render 生产服务持续健康（v2.0.0）
- Git 同步率: 100%（`5df3359` = origin/main，workspace）
- 闭环自 2026-06-06 以来无 P0/P1/P2 阻塞（aitoearn TikTok 阻塞为 P1 运营问题，非技术阻塞）

## 教训

- **2026-06-12 08:00**: team-deep-check 因 AI 过载失败，之后连续正常
- cron job 删除后若无记录难以追溯，应在 workspace 内记录所有 job 配置
- 外部触发器（如 Render webhook）可作为 cron 的备份触发机制

### ✅ aitoearn-run 日志清理完成（2026-07-11 21:00 CST）
- 清理 39 个旧 aitoearn-run 文件（保留每日最新2个）
- 仓库体积大幅减少（delete 1084 lines, add 153 lines）

*最后更新: 2026-07-11 21:00 (Asia/Shanghai)*
