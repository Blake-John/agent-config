---
description: 编排多个 agent 处理复杂任务
agent: planner
subtask: true
---

# 编排命令

为复杂任务编排多个专业 agent：$ARGUMENTS

## 你的任务

1. **分析任务复杂度**并拆分为子任务
2. **为每个子任务选择合适的 agent**
3. **创建带依赖关系的执行计划**
4. **协调执行** — 尽可能并行
5. **汇总结果**为统一输出

## 可用 Agent

| Agent | 专长 | 用途 |
|-------|------|------|
| planner | 实现规划 | 复杂功能设计 |
| arch-designer | 系统设计 | 架构决策 |
| code-reviewer | 代码质量 | 审查变更 |
| security-reviewer | 安全分析 | 漏洞检测 |
| test-specialist | 测试驱动开发 | 功能实现 |
| executor | 构建修复 | 构建错误修复 |
| doc-writer | 文档编写 | 更新文档 |
| refactor-cleaner | 代码清理 | 移除死代码 |

## 编排模式

### 串行执行
```
planner → test-specialist → code-reviewer → security-reviewer
```
适用：后置任务依赖前置结果

### 并行执行
```
         ┌→ security-reviewer
planner →├→ code-reviewer
         └→ arch-designer
```
适用：任务之间独立

### 扇出/扇入
```
         ┌→ agent-1 ─┐
planner →├→ agent-2 ─┼→ 汇总
         └→ agent-3 ─┘
```
适用：需要多方视角

## 协调规则

1. **先计划再执行** — 先创建完整执行计划
2. **最少交接** — 减少上下文切换
3. **尽可能并行** — 独立任务并行执行
4. **清晰边界** — 每个 agent 有明确范围
5. **唯一信源** — 每个工件只有一个 agent 负责
