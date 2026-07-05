# team-coordinator 每时报
**时间**: 2026-07-06 05:01 (Asia/Shanghai) — 卯时报
**触发**: team-coordinator-hourly cron job

---

## 🔴 紧急告警：Token Plan 用量已达上限（新增 P0 阻塞）

| 项目 | 值 |
|------|-----|
| **lastRunStatus** | 🔴 **error** |
| **lastError** | `⚠️ 已达到 Token Plan 用量上限：请升级 Token Plan 套餐或购买积分补充用量。 (2056)` |
| **连续失败** | 3次（02:00 / 03:00 / 04:00 CST） |
| **首次出现** | 2026-07-06 02:00 CST |
| **最后成功** | 2026-07-06 01:03 CST（`team-coordinator-2026-07-06-01.md`） |

---

## 📊 各维度状态（基于 01:03 成功报告 + 手动验证）

| 维度 | 状态 | 详情 |
|------|------|------|
| **Render 生产** | 🟢 | `/api/health` HTTP 200 v2.0.0 ✅（刚验证） |
| **Git 同步** | 🟢 | `160143b` = origin/main ✅（刚验证） |
| **team-coordinator** | 🔴 **Token上限** | 02:00/03:00/04:00 CST 连续3次 Token Plan 用量上限 |
| **team-deep-check** | 🔴 | 连续14+次 LLM timeout，最后成功 07-05 04:20 CST |
| **aitoearn** | 🟢 | SSL自愈稳定（连续37次+无错误） |

---

## 🚨 阻塞清单（更新）

| 优先级 | 事项 | 持续 | 性质 |
|--------|------|------|------|
| 🔴 **P0** | **Token Plan 用量上限** | 02:00 CST 起，约 **3小时** | 账户余额/套餐问题 |
| 🔴 P0 | **team-deep-check 模型超时** | 07-04 16:00 起，约 **13小时** | 供应商+配置缺失 |
| 🔴 P1 | aitoearn TikTok 涨粉 | ~673h+ | 运营问题，需人工 |
| 🟡 P3 | 企业微信回调验证 | 多日 | 需田太平人工确认 |

---

## ✅ 已确认正常项

| 检查项 | 结果 | 时间 |
|--------|------|------|
| Render `/api/health` | HTTP 200 ✅ `{"status":"healthy","name":"鸠摩罗什Bot Agent","version":"2.0.0"}` | 05:01 CST |
| Git HEAD | `160143b` ✅ = origin/main | 05:01 CST |
| origin/main | `160143b` ✅ | - |

---

## 🔍 Token Plan 用量分析

**问题**: MiniMax 账户已达到 Token Plan 用量上限，导致 coordinator cron 任务连续失败。

**消耗估算**（基于 cron runs 数据）:
- coordinator 单次 input_tokens: 14k-75k（平均约 50k）
- 每日 coordinator 运行: 24次
- 每日 token 消耗: 约 1.2M tokens（约 $0.96-3.84/天）
- **小时消耗**: 约 50k-100k tokens/次 × 1次/hr

**可能原因**:
1. Token Plan 套餐额度已用完
2. 深检任务（team-deep-check）大量消耗 token 预算
3. 多个 cron job 并发导致突发消耗

**建议处理**:
1. 登录 MiniMax 账户检查 Token Plan 用量
2. 升级套餐或购买积分补充用量
3. 考虑为 team-deep-check 添加 `timeoutSeconds: 300` 配置以减少 token 消耗
4. 考虑切换到 DeepSeek 作为备选模型

---

## 🎯 本次结论

✅ **Render 生产服务** — HTTP 200 v2.0.0 ✅

✅ **Git 完美同步** — `160143b` = origin/main ✅

🔴 **Token Plan 用量已达上限** — 新增 P0 阻塞，连续3次失败，需充值或升级套餐

🔴 **team-deep-check 模型超时危机** — 连续14+次超时，需配置 `timeoutSeconds`

🔴 **TikTok 涨粉** — 唯一业务阻塞，约673小时+

🟡 **企业微信回调** — P3 遗留，需田太平人工确认

---

## 📋 行动建议

### 🔴 需人工介入（最高优先）

1. **【P0】Token Plan 充值**
   - 登录 MiniMax 账户检查 Token Plan 用量
   - 升级套餐或购买积分补充用量
   - 充值后 coordinator 将自动恢复运行

2. **【P0】team-deep-check 超时修复**
   - 在 Gateway 配置中添加 `"timeoutSeconds": 300` 到 `models.providers.minimax`

3. **【P1】aitoearn TikTok 涨粉**
   - 账号粉丝 < 100，建议手动运营 TikTok 发布内容积累粉丝至 ≥100

---

*team-coordinator — 2026-07-06 05:01 (Asia/Shanghai)*
*状态: 🔴 Token Plan 用量上限 P0 阻塞 + 🔴 deep-check 超时危机*
