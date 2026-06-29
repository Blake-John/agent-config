---
description: Rust 代码审查，关注所有权、安全性和惯用模式
agent: code-reviewer
subtask: true
---

# Rust 审查命令

审查 Rust 代码的惯用模式和最佳实践：$ARGUMENTS

## 审查清单

### 安全性（CRITICAL）

- [ ] 生产路径中没有未检查的 `unwrap()`/`expect()`
- [ ] `unsafe` 块带有 `// SAFETY:` 注释
- [ ] 无 SQL/命令注入
- [ ] 无硬编码密钥

### 所有权（HIGH）

- [ ] 无不必要的 `.clone()`
- [ ] 函数参数中优先使用 `&str` 而非 `String`
- [ ] 函数参数中优先使用 `&[T]` 而非 `Vec<T>`
- [ ] 无多余的生命周期标注

### 错误处理（HIGH）

- [ ] 使用 `?` 传播错误
- [ ] 无被静默忽略的错误（`let _ = result;`）
- [ ] 库代码用 `thiserror`，应用代码用 `anyhow`

### 并发（HIGH）

- [ ] 异步上下文中无阻塞调用
- [ ] 优先使用有界通道
- [ ] `Mutex` 中毒已处理
- [ ] `Send`/`Sync` 约束正确

### 代码质量（MEDIUM）

- [ ] 函数不超过 50 行
- [ ] 无深层嵌套（>4 层）
- [ ] 业务枚举使用穷尽匹配
- [ ] Clippy 警告已处理

## 报告格式

### CRITICAL 问题
- [file:line] 问题描述：修复建议

### HIGH 问题
- [file:line] 问题描述：修复建议

---

**提示**：运行 `cargo clippy -- -D warnings` 和 `cargo fmt --check` 进行自动化检查。
