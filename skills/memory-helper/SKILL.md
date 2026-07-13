---
name: "memory-helper"
description: "自动记忆助手：承诺/决定/待办自动写入文件，防止遗忘"
---

# Memory Helper Skill

## 目标
解决"说完就忘"问题。参考 Hermes 三层记忆架构：Episodic（对话历史）、Semantic（MEMORY.md/USER.md）、Procedural（SKILL.md）。

## 触发规则

### 自动记录（Sync）
说出"记下了"、"会跟进"、"帮我记住"时，立刻写入 `memory/YYYY-MM-DD.md`：
- 待办事项（含负责人、截止时间）
- 重要决定及原因
- 用户要求记忆的内容

### 自动召回（Recall）
用户提到"之前"、"上次"、"记得吗"时，立即 grep 搜索 memory/ 目录

### Session 启动
自动加载 MEMORY.md + 今日日记 + HEARTBEAT.md

## 写入格式
```
## HH:MM CST — 记忆记录
- 讨论：XXX
- 决定：XXX
- 待办：[ ] XXX（负责人：XXX，截止：XXX）
```

## 验收标准
- [ ] 说出"记下了"时自动写入今日日记
- [ ] 用户提"之前"时能召回对应记忆
- [ ] 待办含负责人和截止时间
