# Team Deep Check Report
**时间**: 2026-08-05 00:00 (Asia/Shanghai)

---

## 1. Git 同步状态
**状态**: ⚠️ EXEC 工具异常 (spawn /bin/zsh EAGAIN)
- 无法执行 git fetch/log 命令
- 系统可能存在进程/资源限制

---

## 2. Render 生产健康
**状态**: ⚠️ EXEC 工具异常
- curl 检查无法执行 (相同 EAGAIN 错误)

---

## 3. aitoearn 扫描状态
**状态**: ⚠️ 无法检查
- EXEC 工具异常，无法读取 aitoearn 目录状态

---

## 4. Cron Jobs 列表
| Job ID | Name | 状态 | 下次运行 |
|--------|------|------|----------|
| `77493094-f094-4c1b-975f-855e2683312f` | team-deep-check | ⚠️ error | 2026-08-05 12:00 CST |

**注意**: lastRunStatus = "error"，本 job 自身执行出错

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
- Weather 最后检查: `1752283500` (需转换为可读时间)
- Email/Calendar 未配置检查

---

## 汇总

**整体状态**: 🔴 存在问题

1. **EXEC 工具持续失败** - spawn /bin/zsh EAGAIN 错误，可能原因:
   - 系统进程数达到上限
   - 文件描述符耗尽
   - 内存压力
   
2. **team-deep-check cron job 上次运行状态为 error**
   - 本次报告即为该 job 的执行尝试
   - 由于 EXEC 失败导致无法完成检查

3. **Render 服务健康状态未知** - 无法执行 curl 检查

---

**建议操作**:
- 检查系统资源: `ulimit -a`, `sysctl kern.maxproc`
- 检查 OpenClaw Gateway 进程状态
- 手动执行 `git fetch` 确认网络正常

*报告生成时间: 2026-08-05 00:00 CST*
