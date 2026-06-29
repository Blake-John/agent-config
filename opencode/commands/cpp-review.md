---
description: 全面的 C++ 代码审查，关注内存安全、现代 C++ 惯用法和并发安全
agent: code-reviewer
subtask: true
---

# C++ 代码审查命令

对 C++ 代码进行全面审查：$ARGUMENTS

## 工作流程

1. **识别 C++ 变更**：通过 `git diff` 找出修改的 .cpp/.hpp 文件
2. **运行静态分析**：执行 `clang-tidy` 和 `cppcheck`
3. **内存安全检查**：检查裸 new/delete、缓冲区溢出、use-after-free
4. **并发审查**：分析线程安全、互斥锁使用、数据竞争
5. **现代 C++ 检查**：确保代码遵循 C++17/20 约定

## 审查类别

### CRITICAL（必须修复）

- 裸 `new`/`delete` 未使用 RAII
- 缓冲区溢出和 use-after-free
- 无同步机制的数据竞争
- 通过 `system()` 的命令注入
- 未初始化变量读取
- 空指针解引用

### HIGH（应该修复）

- Rule of Five 违反
- 缺少 `std::lock_guard` / `std::scoped_lock`
- 分离线程未正确处理生命周期
- C 风格强制转换
- 缺少 `const` 正确性

### MEDIUM（考虑修复）

- 不必要的拷贝（值传递而非 `const&`）
- 已知大小的容器缺少 `reserve()`
- 头文件中使用 `using namespace std;`
- 重要的返回值缺少 `[[nodiscard]]`

## 批准标准

| 状态 | 条件 |
|------|------|
| 通过 | 无 CRITICAL 或 HIGH 问题 |
| 警告 | 仅 MEDIUM 问题（谨慎合入） |
| 阻止 | 存在 CRITICAL 或 HIGH 问题 |

## 相关命令

- `/cpp-test` — 先确保测试通过
- `/cpp-build` — 如有构建错误先修复
- `/code-review` — 非 C++ 特定的全面审查
