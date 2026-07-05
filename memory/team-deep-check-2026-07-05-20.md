# team-deep-check 深检报告
**时间**: 2026-07-05 20:00 (Asia/Shanghai) — 酉时报深检
**触发**: team-deep-check cron job

---

## 🚨 紧急告警：team-deep-check 模型超时风暴（连续14次+）

| 项目 | 值 |
|------|-----|
| **lastRunStatus** | 🔴 **error** |
| **lastError** | `The model did not produce a response before the model idle timeout` |
| **lastError run** | 2026-07-05 16:16 CST（08:16:46 UTC），约 **3.8 小时前** |
| **consecutiveErrors** | 🔴 **14+**（07-04 16:00 CST 起持续递增） |
| **最后成功运行** | 2026-07-05 04:20 CST（`team-deep-check-2026-07-05-04.md`） |
| **错误模式** | LLM request timed out — 每次耗时 ~750-970s 后超时 |
| **性质** | MiniMax-M2.7 供应商持续不稳定，深检任务 token 量大，触发 idle timeout |

---

## 📊 各维度状态（基于最近成功报告 + 手动验证）

| 维度 | 状态 | 详情 |
|------|------|------|
| **Render 生产** | 🟢 | `/api/health` HTTP 200 v2.0.0 ✅（刚验证） |
| **Git 同步** | 🟢 | `61cd549` = origin/main ✅（刚验证） |
| **team-coordinator** | 🟢 | 19:31 酉时报正常（`team-coordinator-2026-07-05-19.md`） |
| **team-deep-check** | 🔴 **连续超时** | consecutiveErrors=14+，最后成功 04:20 CST |
| **aitoearn** | 🟢 | **SSL自愈稳定**（19:17 执行无 SSL 错误），仅 TikTok 粉丝不足 |

---

## 🔍 模型超时根因分析

**MiniMax-M2.7 持续超时的直接原因**:

1. **`timeoutSeconds` 未配置** — `models.providers.minimax` 下没有任何 `timeoutSeconds` 设置，默认值对深度检查任务不足
2. **深检任务 token 消耗极大** — 单次深检加载：
   - MEMORY.md + 近期深检报告 + cron runs 历史（50条） + sessions列表 + git状态
   - input_tokens 经常达到 100,000-150,000+
3. **供应商持续不稳定** — 07-04 16:00 CST 起，MiniMax API 响应极慢，触发 idle timeout

**建议修复**（需田太平确认）:
```json
"models": {
  "providers": {
    "minimax": {
      "timeoutSeconds": 300
    }
  }
}
```

---

## ✅ 已确认正常项（07-05 手动验证）

| 检查项 | 结果 | 时间 |
|--------|------|------|
| Render `/api/health` | HTTP 200 ✅ | 20:03 CST |
| Git HEAD | `61cd549` ✅ | - |
| origin/main | `61cd549` ✅ | - |
| aitoearn 最新 | 19:17 ✅ 无SSL错误 | 19:17 CST |

---

## 🔴 阻塞清单

| 优先级 | 事项 | 持续 | 性质 |
|--------|------|------|------|
| 🔴 **P0** | **team-deep-check 模型超时** | 07-04 16:00 起，约 16h | 供应商问题 + 配置缺失 |
| 🔴 P1 | aitoearn TikTok 涨粉 | ~665h+ | 运营问题，需人工 |
| 🟡 P3 | 企业微信回调验证 | 多日未解决 | 需田太平人工确认 |

---

## ✅ 已解决

| 事项 | 之前 | 现在 |
|------|------|------|
| aitoearn SSL EOF | 🔴 持续22天+ | 🟢 **已自愈**，连续35次+无错误 |
| 模型偶发超时 | ⚠️ 偶发 | 🔴 **持续风暴**，需配置 timeoutSeconds |

---

## 🎯 本次结论

✅ **Render 生产服务** — `/api/health` HTTP 200 v2.0.0 ✅

✅ **Git 完美同步** — `61cd549` = origin/main ✅

✅ **aitoearn SSL 自愈稳定** — 连续35次+无错误执行 ⭐

🔴 **team-deep-check 处于危机状态** — 连续14+次 LLM timeout，最后成功 04:20 CST，需配置 `timeoutSeconds`

🔴 **唯一真实业务阻塞: TikTok涨粉** — 粉丝 < 100 持续665小时+，无法自动接单

🟡 **企业微信回调验证** — P3 遗留，需田太平人工操作

---

## 📋 行动建议

### 🔴 需人工介入（无法自动化）

1. **team-deep-check 超时修复**（最高优先）:
   - 在 Gateway 配置中添加 `"timeoutSeconds": 300` 到 `models.providers.minimax`
   - 或切换到 DeepSeek 作为备选模型

2. **aitoearn TikTok 涨粉** — 账号粉丝 < 100，建议手动运营 TikTok 发布内容积累粉丝至 ≥100

### 🟡 建议跟进

3. **企业微信回调验证** — 需田太平在企业微信应用后台"发送测试"确认

---

## 📅 下一个深检时间

**2026-07-06 00:00 CST**（子时报，约4小时后）
> ⚠️ 注意：下次深检仍可能因模型超时失败，建议优先修复 timeoutSeconds 配置

---

*team-deep-check — 2026-07-05 20:00 (Asia/Shanghai)*
*状态: 🔴 危机运行中，consecutiveErrors=14+，需紧急介入*
