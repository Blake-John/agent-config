# 循环启动命令

启动托管自主循环模式，带安全默认值。

## 用法

`/loop-start [pattern] [--mode safe|fast]`

- `pattern`：`sequential`、`continuous-pr`、`rfc-dag`、`infinite`
- `--mode`：
  - `safe`（默认）：严格质量门禁和检查点
  - `fast`：减少门禁以提高速度

## 流程

1. 确认仓库状态和分支策略
2. 选择循环模式和模型层级策略
3. 启用所选模式所需的 hooks/配置
4. 创建循环计划，在 `.claude/plans/` 下编写运行手册
5. 打印启动和监控循环的命令

## 安全检查

- 首次循环迭代前验证测试通过
- 确保循环有明确的停止条件

## 参数

$ARGUMENTS：
- `<pattern>` 可选（`sequential|continuous-pr|rfc-dag|infinite`）
- `--mode safe|fast` 可选
