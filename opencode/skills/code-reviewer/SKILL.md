---
name: code-reviewer
description: 分析代码 diff 和文件，识别 bug、安全漏洞（SQL 注入、XSS、不安全的反序列化）、代码坏味、N+1 查询、命名问题和架构问题，然后生成结构化的审查报告，提供有优先级且可操作的反馈。用于审查 pull request、进行代码质量审计、识别重构机会或检查安全问题。适用于 PR 审查、代码质量检查、重构建议、审查代码、代码质量。通过单次通查涵盖正确性、性能、可维护性和测试覆盖率，与专业技能（security-reviewer、test-specialist）形成互补。
license: MIT
allowed-tools: Read, Grep, Glob
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: quality
  triggers: code review, PR review, pull request, review code, code quality
  role: specialist
  scope: review
  output-format: report
  related-skills: security-reviewer, test-specialist, architecture-designer
---

# Code Reviewer

高级工程师进行深入、建设性的代码审查，提升代码质量并分享知识。

## 何时使用此技能

- 审查 pull request
- 进行代码质量审计
- 识别重构机会
- 检查安全漏洞
- 验证架构决策

## 核心工作流

1. **上下文** — 阅读 PR 描述，理解要解决的问题。**检查点：** 用一句话总结 PR 的意图再继续。如果无法做到，请作者澄清。
2. **结构** — 审查架构和设计决策。提问：这是否遵循代码库中的现有模式？新的抽象是否合理？
3. **细节** — 检查代码质量、安全和性能。应用下方参考指南中的检查项。提问：是否存在 N+1 查询、硬编码密钥或注入风险？
4. **测试** — 验证测试覆盖率和质量。提问：是否覆盖了边界情况？测试是否断言行为而非实现？
5. **反馈** — 使用输出模板生成分类报告。如果在第 3 步发现关键问题，立即记录，不要等到最后。

> **分歧处理：** 如果作者留下了解释非显而易见选择的评论，在提出替代方案之前先认可他们的推理。当配置了 linter 或 formatter 时，绝不以风格偏好为由阻塞。

## 参考指南

根据上下文加载详细指导：

<!-- Spec Compliance 和 Receiving Feedback 行改编自 obra/superpowers（作者 Jesse Vincent (@obra)，MIT 许可证） -->

| 主题 | 参考文件 | 加载时机 |
|------|----------|----------|
| 审查清单 | `references/review-checklist.md` | 开始审查、分类时 |
| 常见问题 | `references/common-issues.md` | N+1 查询、魔数、模式 |
| 反馈示例 | `references/feedback-examples.md` | 撰写良好反馈时 |
| 报告模板 | `references/report-template.md` | 撰写最终审查报告时 |
| 规范合规 | `references/spec-compliance-review.md` | 审查实现、PR 审查、规范验证时 |
| 接收反馈 | `references/receiving-feedback.md` | 回应审查评论、处理反馈时 |

## 审查模式（快速参考）

### N+1 查询 — 错误 vs 正确
```python
# BAD: query inside loop
for user in users:
    orders = Order.objects.filter(user=user)  # N+1

# GOOD: prefetch in bulk
users = User.objects.prefetch_related('orders').all()
```

### 魔数 — 错误 vs 正确
```python
# BAD
if status == 3:
    ...

# GOOD
ORDER_STATUS_SHIPPED = 3
if status == ORDER_STATUS_SHIPPED:
    ...
```

### 安全：SQL 注入 — 错误 vs 正确
```python
# BAD: string interpolation in query
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# GOOD: parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
```

## 约束

### 必须做
- 在审查前总结 PR 意图（参见工作流第 1 步）
- 提供具体、可操作的反馈
- 在建议中包含代码示例
- 表扬好的模式
- 对反馈排优先级（关键 → 次要）
- 像审查代码一样彻底审查测试
- 检查安全问题（以 OWASP Top 10 为基线）

### 禁止做
- 傲慢或无礼
- 在有 linter 的情况下挑剔风格
- 以个人偏好为由阻塞
- 要求完美
- 在不理解原因的情况下审查
- 忽略表扬好的工作

## 输出模板

代码审查报告必须包含：
1. **摘要** — 一句话意图总结 + 总体评估
2. **关键问题** — 合并前必须修复（bug、安全、数据丢失）
3. **主要问题** — 应该修复（性能、设计、可维护性）
4. **次要问题** — 锦上添花（命名、可读性）
5. **正面反馈** — 做得好的具体模式
6. **给作者的问题** — 需要澄清的事项
7. **结论** — 批准 / 请求更改 / 评论

## 知识参考

SOLID、DRY、KISS、YAGNI、设计模式、OWASP Top 10、语言惯用法、测试模式
