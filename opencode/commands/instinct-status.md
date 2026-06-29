---
description: 显示已学习的 instinct（项目 + 全局）及置信度
agent: build
---

# Instinct 状态命令

显示 continuous-learning-v2 的 instinct 状态：$ARGUMENTS

## 你的任务

运行：

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" status
```

如果 `CLAUDE_PLUGIN_ROOT` 不可用，使用：

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py status
```

## 行为说明

- 输出包含项目作用域和全局作用域的 instinct
- ID 冲突时项目 instinct 覆盖全局 instinct
- 按领域分组显示，带置信度条
- v2.1 不支持额外过滤器
