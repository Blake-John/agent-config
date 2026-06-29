---
description: 修复 C++ 构建错误、CMake 问题和链接错误
agent: build
subtask: true
---

# C++ 构建修复命令

逐步修复 C++ 构建错误：$ARGUMENTS

## 工作流程

1. **运行诊断**：执行 `cmake --build`、`clang-tidy`、`cppcheck`
2. **解析错误**：按文件分组，按严重程度排序
3. **逐步修复**：每次只修复一个错误
4. **验证每次修复**：每次变更后重新构建
5. **报告摘要**：显示修复和剩余问题

## 何时使用

- `cmake --build build` 失败
- 链接错误（未定义引用、多重定义）
- 模板实例化失败
- 包含/依赖问题
- 拉取变更后构建中断

## 诊断命令

```bash
cmake -B build -S .
cmake --build build 2>&1 | head -100
clang-tidy src/*.cpp -- -std=c++17
cppcheck --enable=all src/
```

## 常见错误

| 错误 | 典型修复 |
|------|----------|
| `undeclared identifier` | 添加 `#include` 或修正拼写 |
| `no matching function` | 修正参数类型或添加重载 |
| `undefined reference` | 链接库或添加实现 |
| `multiple definition` | 使用 `inline` 或移到 .cpp |
| `CMake Error` | 修复 CMakeLists.txt 配置 |

## 修复策略

1. **先编绎错误** — 代码必须能编绎
2. **再链接错误** — 解析未定义引用
3. **最后警告** — 使用 `-Wall -Wextra` 修复
4. **每次一个修复** — 每次变更后验证
5. **最小变更** — 只修复，不重构

## 停止条件

- 同一错误持续 3 次仍未解决
- 修复引入了更多错误
- 需要架构层面的变更
- 缺少外部依赖

## 相关命令

- `/cpp-test` — 构建成功后运行测试
- `/cpp-review` — 审查代码质量
