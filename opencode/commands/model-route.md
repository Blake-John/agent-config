# 模型路由命令

根据任务复杂度和预算推荐最佳模型层级。

## 用法

`/model-route [task-description] [--budget low|med|high]`

## 路由规则

- `haiku`：确定性的、低风险机械变更
- `sonnet`：实现和重构的默认选择
- `opus`：架构设计、深度审查、模糊需求

## 输出要求

- 推荐模型
- 置信度级别
- 选择此模型的原因
- 首次尝试失败的备用模型

## 参数

$ARGUMENTS：
- `[task-description]` 可选自由文本
- `--budget low|med|high` 可选
