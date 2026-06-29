---
description: 对 Rust 代码强制执行 TDD 工作流
agent: test-specialist
subtask: true
---

# Rust 测试命令

对 Rust 代码强制执行测试驱动开发：$ARGUMENTS

## 测试命令

```bash
cargo test                    # 运行所有测试
cargo test -- --nocapture     # 显示输出
cargo test --lib              # 仅单元测试
cargo test --test integration # 仅集成测试
cargo test --doc              # 仅文档测试
cargo llvm-cov                # 覆盖率
cargo llvm-cov --fail-under-lines 80  # 覆盖率门禁
```

## 测试类型

- **单元测试**：`#[cfg(test)] mod tests`，在源文件内
- **集成测试**：`tests/` 目录下
- **文档测试**：代码文档中的 `///` 示例
- **属性测试**：使用 `proptest` 框架

---

**强制要求**：先写测试再实现。禁止跳过 RED 阶段。
