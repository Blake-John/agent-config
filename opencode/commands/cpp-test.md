---
description: 对 C++ 代码强制执行 TDD 工作流，使用 GoogleTest，验证覆盖率
---

# C++ 测试命令

对 C++ 代码强制执行测试驱动开发：$ARGUMENTS

## TDD 循环

```
RED     → 编写失败的 GoogleTest 测试
GREEN   → 实现最简 C++ 代码
REFACTOR → 保持测试通过的前提下改进
```

## 覆盖率

- 生成：`cmake -B build-cov -DCMAKE_CXX_FLAGS="--coverage" && cmake --build build-cov`
- 报告：`lcov --capture --directory build-cov --output-file coverage.info --exclude '/usr/*' 'test/*'`
- 验证：`lcov --summary coverage.info`
- 目标：标准代码 80%+，关键逻辑 100%
