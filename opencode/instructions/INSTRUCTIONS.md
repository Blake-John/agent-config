# OpenCode 开发指令

本文件整合了 OpenCode 开发过程中的核心规则和指南。

---

## 安全指南（关键）

### 强制要求

所有代码必须满足以下安全要求，具体实现细节参见 **security-reviewer** agent：

- **密钥管理**：所有密钥使用环境变量，禁止硬编码
- **输入校验**：所有用户输入必须校验（SQL 注入、XSS、命令注入防护）
- **认证授权**：敏感端点必须验证身份和权限
- **错误处理**：错误信息不泄露敏感数据
- **安全配置**：CSRF 防护、限流、安全头

### 安全事件响应

发现安全问题时：

1. 立即停止
2. 使用 **security-reviewer** agent
3. 优先修复 CRITICAL 级别问题
4. 轮换所有已暴露的密钥
5. 审查整个代码库类似问题

---

## 编码规范

详见 [CODING-STYLE.md](./CODING-STYLE.md)。核心原则：

- **不可变性**：始终创建新对象，永不修改现有对象
- **KISS**：最简单的方案往往是最好的
- **DRY**：提取重复逻辑，但不要过早抽象
- **YAGNI**：不构建当前不需要的功能

---

## 测试要求

### 最低覆盖率：80%

必须覆盖三种测试类型：

1. **单元测试** — 函数、工具、组件级别
2. **集成测试** — API 端点、数据库操作
3. **E2E 测试** — 关键用户流程

### TDD 工作流

```
1. 编写测试（RED）→ 预期失败
2. 最小实现（GREEN）→ 通过测试
3. 重构（IMPROVE）→ 优化代码
4. 验证覆盖率 ≥ 80%
```

### 测试失败排查

1. 检查测试是否隔离
2. 验证 mock 是否正确
3. 优先修复实现，而不是修改测试（除非测试本身错误）

---

## Git 工作流

### 提交信息格式

```
<type>: <description>

<optional body>
```

类型：feat, fix, refactor, docs, test, chore, perf, ci

### 功能实现流程

1. **研究优先** — 搜索已有实现和库文档，避免重复造轮子
2. **规划优先** — 使用 **planner** agent 创建实现计划
3. **TDD 实现** — 使用 **test-specialist** agent 编写测试→实现→重构
4. **代码审查** — 使用 **code-reviewer** agent 审查代码
5. **文档更新** — 使用 **doc-writer** agent 更新文档
6. **提交推送** — 详细提交信息，遵循 conventional commits

---

## Agent 编排

### 可用 Agent

| Agent | 职责 | 使用时机 |
|-------|------|----------|
| orchestrator | 编排调度中心，统一调度所有 subagent | 默认入口，复杂任务的主控 |
| executor | 任务执行，测试运行，代码重构，进程监控 | 具体执行任务、运行测试、重构代码 |
| explorer | 基于 codegraph 探索项目结构和代码 | 理解不熟悉的代码库 |
| websearcher | 网络搜索和信息整理 | 需要查找外部资料、文档 |
| planner | 制定实现计划 | 复杂功能、重构的前置规划 |
| arch-designer | 系统架构设计 | 架构决策、技术选型 |
| code-reviewer | 代码审查 | 编写代码后立即审查 |
| test-specialist | 测试驱动开发 | 新功能、bug 修复 |
| security-reviewer | 安全分析 | 提交前安全检查 |
| refactor-cleaner | 死代码清理、代码整合 | 代码维护、重构后清理 |
| doc-writer | 文档编写和更新 | 更新文档、生成技术文档 |

### 自动调度规则

以下场景无需用户提示：

1. 复杂功能请求 → 使用 **planner** agent
2. 代码刚编写/修改 → 使用 **code-reviewer** agent
3. Bug 修复或新功能 → 使用 **test-specialist** agent
4. 架构决策 → 使用 **arch-designer** agent

### 调度策略

- 用户指定则按用户要求执行
- 未指定时由 orchestrator 综合判断任务复杂度后调度
- 同一时间只有一个任务处于进行中状态
- executor 是唯一具备循环执行能力的 agent

---

## 通用模式

### API 响应格式

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  meta?: {
    total: number
    page: number
    limit: number
  }
}
```

### Repository 模式

```typescript
interface Repository<T> {
  findAll(filters?: Filters): Promise<T[]>
  findById(id: string): Promise<T | null>
  create(data: CreateDto): Promise<T>
  update(id: string, data: UpdateDto): Promise<T>
  delete(id: string): Promise<void>
}
```

---

## 成功标准

- 所有测试通过（覆盖率 ≥ 80%）
- 无安全漏洞
- 代码可读且可维护
- 性能在可接受范围内
- 满足用户需求

## 可用命令

- `/plan` — 创建实现计划
- `/test` — 执行 TDD 工作流
- `/code-review` — 审查代码变更
- `/security` — 运行安全检查
- `/refactor-clean` — 移除死代码
- `/orchestrate` — 多 agent 协作工作流
