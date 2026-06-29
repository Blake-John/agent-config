---
description: Python 代码审查，关注类型安全、错误处理和性能
agent: code-reviewer
subtask: true
---

# Python 审查命令

审查 Python 代码的质量和最佳实践：$ARGUMENTS

## 审查类别

### CRITICAL（必须修复）

- 硬编码凭据、API 密钥
- SQL 注入（使用参数化查询）
- 命令注入（使用 `shlex.quote()`）
- 不安全的反序列化（`pickle` 来自不可信源）
- 路径遍历（校验文件名）

### HIGH（应该修复）

- 函数参数缺少类型提示
- 可变默认参数
- 未使用上下文管理器处理资源
- 裸露的 `except:` 捕获隐藏错误
- 不使用 `zip()`/`enumerate()` 的索引循环
- 缺少 `__slots__` 的类
- 可变对象作为类属性

### MEDIUM（考虑修复）

- 魔数无命名常量
- 长函数（>50 行）
- 深层嵌套（>4 层）
- 未使用的导入
- TODO/FIXME 注释
- 缺少文档字符串
- 可变的 `__init__` 参数

## 验证

运行：

```bash
mypy .                     # 类型检查
ruff check .               # lint
black --check .            # 格式化
pytest --cov=app           # 测试和覆盖率
```
