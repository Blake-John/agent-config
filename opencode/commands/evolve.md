---
description: 分析 instinct 并建议或生成演化的组件
agent: build
---

# 演化命令

分析并演化 continuous-learning-v2 中的 instinct：$ARGUMENTS

## 你的任务

运行：

```bash
python3 "<skills_path>/continuous-learning-v2/scripts/instinct-cli.py" evolve $ARGUMENTS
```

`<skills_path>` 可能是：

- `~/.agents/skills`
- `~/.config/opencode/skills`
- `./.agents/skills`

## 支持的参数（v2.1）

- 无参数：仅分析
- `--generate`：同时在 `evolved/{skills,commands,agents}` 下生成文件

## 行为说明

- 使用项目 + 全局 instinct 进行分析
- 通过触发词和领域聚类显示 skill/command/agent 候选
- 显示项目 → 全局的提建议候选
- 使用 `--generate` 时，输出路径为项目上下文：`<project_path>/evolved/`
