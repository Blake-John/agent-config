---
name: agent-engine
description: Orchestrator 的扩展，专注于长运行任务的跨会话管理。用于识别长运行任务、管理多个会话的执行、跨会话传递进度和上下文、支持暂停和恢复。当用户需要构建复杂的、需要多会话完成的项目时，当用户提到需要自主编码、长运行 agent、多会话开发、增量开发时，必须使用此 skill。
license: MIT
metadata:
  author: ECC
  version: "2.0.0"
  domain: agent-orchestration
  triggers: 长运行任务, 多会话开发, 自主编码, 增量开发, 跨会话管理, long-running agent, multi-session, autonomous coding
  role: specialist
  scope: orchestration
  output-format: structured
  related-skills: orchestrator, planner, executor
  languages: all
  tools: Read Write Edit Bash Todowrite
  requires-installation: false
  auto-sync: false
  local-only: true
---

# Agent Engine

Orchestrator 的扩展，专注于长运行任务的跨会话管理。

## 定位

Agent-Engine 是 Orchestrator 的扩展，专注于长运行任务的跨会话管理。

## 触发场景

当用户有以下需求时，必须使用此 skill：

- 需要构建复杂的、多会话完成的项目
- 需要实现长运行自主编码
- 需要增量开发工作流
- 需要多会话跨上下文窗口的持续开发
- 需要功能级别的进度追踪
- 用户明确提及需要使用这个 skill

## 核心功能

### 1. 识别长运行任务

识别需要多个会话完成的任务。

**识别标准**：
- 任务复杂度高，无法在单个会话内完成
- 任务需要多个阶段（规划、实现、测试、审查）
- 任务需要跨多个文件或模块
- 用户明确表示需要多会话完成

### 2. 管理多个会话的执行

管理多个会话的执行顺序。

**管理内容**：
- 会话的创建和销毁
- 会话的执行顺序
- 会话之间的依赖关系
- 会话的暂停和恢复

### 3. 跨会话传递进度和上下文

跨会话传递进度和上下文，确保任务连续性。

**传递内容**：
- 任务的当前状态
- 已完成的工作
- 未完成的工作
- 遇到的问题
- 重大决策

### 4. 支持暂停和恢复

支持任务的暂停和恢复。

**暂停场景**：
- 用户主动暂停
- 遇到阻塞问题
- 资源限制
- 时间限制

**恢复场景**：
- 用户主动恢复
- 阻塞问题解决
- 资源可用
- 时间允许

## 与 Orchestrator 的关系

```
用户请求
   ↓
Orchestrator（调度中心）
   ↓
任务类型？
   ├─ 单次任务 → 直接调度 Agent
   └─ 长运行任务 → 调用 Agent-Engine
                      ↓
                  Agent-Engine（跨会话管理）
                      ↓
                  识别长运行任务、管理会话、传递进度
                      ↓
                  调用其他 Agent 执行具体任务
```

- Orchestrator 负责单次任务的调度
- Agent-Engine 负责长运行任务的跨会话管理
- Orchestrator 可以调用 Agent-Engine 来处理长运行任务

## 与其他 Agent 的关系

| 组件 | 关系 |
|------|------|
| **plan.md** | 宏观规划文件，记录整体计划 |
| **feature_list.json** | 微观追踪文件，记录功能实现状态 |
| **agent-progress.md** | 进度文件，记录跨会话执行进度 |

## 工作流程

### 1. 初始化

Orchestrator 调用 Agent-Engine 初始化长运行任务。

```
1. 接收长运行任务
   ↓
2. 识别任务类型和复杂度
   ↓
3. 创建会话管理结构
   ↓
4. 创建计划（plan.md）
    ↓
5. 创建功能列表（feature_list.json）
   ↓
6. 初始化进度文件（agent-progress.md）
```

### 2. 会话管理

Agent-Engine 管理多个会话的执行。

```
1. 读取 plan.md 了解整体规划
   ↓
2. 读取 feature_list.json 选择要实现的功能
   ↓
3. 读取 agent-progress.md 了解当前进度
   ↓
4. 执行任务
   ↓
5. 更新 feature_list.json 的 passes 状态
   ↓
6. 更新 agent-progress.md 记录进度
   ↓
7. 检查是否需要继续
   - 如果有更多功能 → 继续下一个会话
   - 如果所有功能完成 → 结束
```

### 3. 进度传递

Agent-Engine 跨会话传递进度和上下文。

**传递内容**：
- 任务的当前状态
- 已完成的工作
- 未完成的工作
- 遇到的问题
- 重大决策

**传递方式**：
- 更新 agent-progress.md
- 更新 feature_list.json
- 更新 plan.md（如需要）

### 4. 状态管理

Agent-Engine 管理任务的状态，支持暂停和恢复。

**状态类型**：
- pending：待执行
- in_progress：执行中
- paused：暂停
- completed：已完成
- failed：失败

**状态转换**：
```
pending → in_progress → completed
pending → in_progress → paused → in_progress → completed
pending → in_progress → failed
```

### 5. 完成

Agent-Engine 汇总结果，生成报告。

```
1. 汇总 feature_list.json 的结果
   ↓
2. 生成最终报告
   ↓
3. 更新 agent-progress.md
   ↓
4. 通知 Orchestrator 任务完成
```

## 核心组件

### 1. plan.md

宏观规划，记录整体计划。

**格式**：
```markdown
# 实现计划: [功能名称]

## 概述
[2-3 句摘要]

## 需求
- [需求 1]
- [需求 2]

## 架构变更
- [变更 1: 文件路径和描述]
- [变更 2: 文件路径和描述]

## 实现阶段

### 阶段 1: [阶段名称]
1. **[步骤名称]** (文件: path/to/file.ts)
   - 行动: 要采取的具体行动
   - 原因: 此步骤的原因
   - 依赖: 无 / 需要步骤 X
   - 风险: 低/中/高

### 阶段 2: [阶段名称]
...

## 测试策略
- 单元测试: [要测试的文件]
- 集成测试: [要测试的流程]
- E2E 测试: [要测试的用户旅程]

## 风险与缓解措施
- **风险**: [描述]
  - 缓解: [如何处理]

## 成功标准
- [ ] 标准 1
- [ ] 标准 2
```

### 2. feature_list.json

微观追踪，用于追踪具体功能的实现状态。

**格式**：
```json
{
  "features": [
    {
      "id": "1",
      "category": "functional",
      "description": "功能描述",
      "steps": [
        "步骤 1: 描述",
        "步骤 2: 描述",
        "步骤 3: 描述"
      ],
      "passes": false,
      "priority": "high"
    }
  ]
}
```

**字段说明**：
- id：功能 ID
- category：功能类别（functional/non-functional）
- description：功能描述
- steps：实现步骤
- passes：是否通过（true/false）
- priority：优先级（high/medium/low）

### 3. agent-progress.md

进度文件，记录跨会话的执行进度。

**格式**：
```markdown
# 进度追踪

## 执行进度

**当前任务**: [任务名称]
**总体进度**: [已完成/总数] ([百分比]%)
**当前状态**: [执行中/验证中/修复中]

### 子任务列表
- [x] 子任务 1: 已完成
- [ ] 子任务 2: 执行中
- [ ] 子任务 3: 待执行

---

## 历史记录

### [YYYY-MM-DD HH:mm:ss] [任务名称]

**完成的任务**:
- 完成了什么任务

**实现的功能**:
- 实现了什么功能

**遇到的问题**:
- 问题: 描述

**重大决策**:
- 决策: 原因

### [YYYY-MM-DD HH:mm:ss] [上一个任务]
...
```

## 最佳实践

1. **识别长运行任务** - 准确识别需要多会话完成的任务
2. **管理会话顺序** - 合理安排会话的执行顺序
3. **传递进度和上下文** - 确保跨会话的进度和上下文传递
4. **支持暂停和恢复** - 支持任务的暂停和恢复
5. **保持状态一致** - 确保状态的一致性

## 常见失败模式及解决方案

| 问题 | 解决方案 |
|------|---------|
| 无法识别长运行任务 | 使用识别标准进行判断 |
| 会话顺序混乱 | 使用 plan.md 管理会话顺序 |
| 进度丢失 | 使用 agent-progress.md 追踪进度 |
| 上下文丢失 | 使用 feature_list.json 传递上下文 |
| 状态不一致 | 使用状态管理机制保持一致 |

## 参考文件

- [feature_list.json](./references/feature_list.json)：功能列表示例
- [agent-progress.md](./references/agent-progress.md)：进度文件示例
