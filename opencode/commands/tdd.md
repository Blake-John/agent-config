---
description: 强制执行 TDD 工作流，覆盖率 80%+
agent: test-specialist
subtask: true
---

# TDD 命令

使用严格的测试驱动开发实现以下功能：$ARGUMENTS

## TDD 循环

```
RED → GREEN → REFACTOR → REPEAT
```

1. **RED**：先编写失败的测试
2. **GREEN**：编写最简代码通过测试
3. **REFACTOR**：保持测试通过的前提下改进代码
4. **REPEAT**：重复直到功能完成

## 覆盖率要求

| 代码类型 | 最低要求 |
|---------|----------|
| 标准代码 | 80% |
| 金融计算 | 100% |
| 认证逻辑 | 100% |
| 安全关键代码 | 100% |

---

**强制要求**：必须先写测试再写实现。禁止跳过 RED 阶段。
