---
name: agent-harness-construction
description: 设计和优化 AI Agent 的行动空间、工具定义和观察格式，以提高任务完成率。用于改进 agent 的规划、工具调用、错误恢复和收敛能力。
license: MIT
metadata:
  author: ECC
  version: "1.0.0"
  domain: agent-optimization
  triggers: agent 优化, 工具设计, 行动空间, 错误恢复, 完成率, agent harness, tool design, action space
  role: specialist
  scope: optimization
  output-format: structured
  related-skills: orchestrator, executor, code-reviewer
  languages: all
  tools: Read Write Edit
  requires-installation: false
  auto-sync: false
  local-only: true
---

# Agent Harness Construction

使用此 skill 来改进 agent 的规划、工具调用、错误恢复和收敛能力。

## 核心模型

Agent 输出质量受以下因素约束：

1. **行动空间质量** - 工具定义是否清晰
2. **观察质量** - 工具返回结果是否清晰
3. **恢复质量** - 错误恢复能力
4. **上下文预算质量** - 上下文管理

## 行动空间设计

1. 使用稳定、明确的工具名称
2. 保持输入 schema 优先且窄
3. 返回确定性的输出形状
4. 避免全能工具，除非隔离不可能

## 粒度规则

| 工具类型 | 使用场景 |
|----------|----------|
| **micro-tools** | 高风险操作（部署、迁移、权限） |
| **medium-tools** | 常见的编辑/读取/搜索循环 |
| **macro-tools** | 当往返开销是主要成本时 |

## 观察设计

每个工具响应应包含：

```json
{
  "status": "success|warning|error",
  "summary": "一行结果摘要",
  "next_actions": ["可执行的后续行动"],
  "artifacts": ["文件路径/ID"]
}
```

## 错误恢复契约

每个错误路径应包含：

| 元素 | 说明 |
|------|------|
| **根因提示** | 错误的根本原因 |
| **安全重试指令** | 如何安全地重试 |
| **明确的停止条件** | 何时停止重试 |

## 上下文预算

1. 保持系统提示最小且不变
2. 将大型指导移至按需加载的 skills
3. 优先引用文件而非内联长文档
4. 在阶段边界压缩，而非任意 token 阈值

## 架构模式指导

| 模式 | 适用场景 |
|------|----------|
| **ReAct** | 探索性任务，路径不确定 |
| **Function-calling** | 结构化确定性流程 |
| **Hybrid（推荐）** | ReAct 规划 + 类型化工具执行 |

## 基准测试

追踪指标：

| 指标 | 说明 |
|------|------|
| **completion rate** | 完成率 |
| **retries per task** | 每任务重试次数 |
| **pass@1** | 一次通过率 |
| **pass@3** | 三次通过率 |
| **cost per successful task** | 每成功任务成本 |

## 反模式

| 反模式 | 说明 |
|--------|------|
| **工具重叠** | 过多重叠语义的工具 |
| **不透明输出** | 工具输出无恢复提示 |
| **无后续步骤** | 仅有错误输出，无后续步骤 |
| **上下文过载** | 包含无关引用 |

## 应用到现有 Agent

### Orchestrator 优化

- **行动空间设计**：明确调度工具的定义
- **错误恢复**：agent 调用失败时的恢复策略
- **观察设计**：agent 返回结果的格式

### Executor 优化

- **粒度规则**：任务执行工具的粒度
- **观察设计**：执行结果的格式
- **错误恢复**：执行失败时的重试策略

### Explorer 优化

- **输出格式**：探索结果的格式
- **上下文预算**：项目信息的管理
- **行动空间**：codegraph 工具的定义

### 其他 Agent 优化

- **工具定义**：每个 agent 的工具定义
- **错误处理**：统一的错误处理策略
- **观察格式**：统一的输出格式

## 最佳实践

1. **明确工具定义** - 每个工具都有清晰的输入输出
2. **统一输出格式** - 所有工具返回相同格式的结果
3. **错误恢复优先** - 每个错误都有恢复策略
4. **上下文精简** - 只传递必要的上下文
5. **渐进式优化** - 逐步优化，不要一次性改变太多

## 示例

### 工具响应示例

```json
{
  "status": "success",
  "summary": "成功找到 login 函数",
  "next_actions": [
    "查看 login 函数的调用者",
    "分析 login 函数的依赖关系"
  ],
  "artifacts": [
    "src/lib/auth.ts:15"
  ]
}
```

### 错误响应示例

```json
{
  "status": "error",
  "summary": "未找到 login 函数",
  "root_cause": "函数名可能不同，可能是 loginAsync 或 authenticate",
  "retry_instruction": "尝试搜索 authenticate 或 loginAsync",
  "stop_condition": "如果连续 3 次搜索未找到，停止并报告"
}
```
