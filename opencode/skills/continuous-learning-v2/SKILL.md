---
name: continuous-learning-v2
description: Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring, and evolves them into skills/commands/agents. v2.1 adds project-scoped instincts to prevent cross-project contamination.
origin: ECC
version: 2.1.0
---

# Continuous Learning v2.1 - Instinct 架构
基于本能的学习系统

一个先进的学习系统，通过原子化的"本能（instincts）"——带有置信度评分的小型学习行为——将你的 Claude Code 会话转化为可复用的知识。

**v2.1** 新增了**项目作用域本能（project-scoped instincts）**——React 模式保留在 React 项目中，Python 约定保留在 Python 项目中，而通用模式（如"始终验证输入"）则全局共享。

## 何时启用

- 设置从 Claude Code 会话自动学习
- 通过 hooks 配置基于本能的行为提取
- 调整学习行为的置信度阈值
- 审查、导出或导入本能库
- 将本能演化为完整的 skills、commands 或 agents
- 管理项目作用域与全局本能
- 将本能从项目作用域提升为全局作用域

## v2.1 新增内容

| 功能 | v2.0 | v2.1 |
|---------|------|------|
| 存储 | 全局 (~/.claude/homunculus/) | 项目作用域 (projects/<hash>/) |
| 作用域 | 所有本能随处适用 | 项目作用域 + 全局 |
| 项目检测 | 无 | git remote URL / repo 路径 |
| 提升机制 | 无 | 在 2+ 项目中出现时，项目 → 全局 |
| 命令 | 4 个 (status/evolve/export/import) | 6 个 (+promote/projects) |
| 跨项目 | 存在污染风险 | 默认隔离 |

## v2 新增内容（相对于 v1）

| 功能 | v1 | v2 |
|---------|----|----|
| 观察方式 | Stop hook（会话结束） | PreToolUse/PostToolUse（100% 可靠） |
| 分析方式 | 主上下文 | 后台 agent (Haiku) |
| 粒度 | 完整 skills | 原子化"本能（instincts）" |
| 置信度 | 无 | 0.3-0.9 加权 |
| 演化方式 | 直接生成 skill | 本能 -> 聚类 -> skill/command/agent |
| 共享方式 | 无 | 导出/导入本能 |

## 本能模型 (Instinct Model)

本能是一个小型学习行为：

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
scope: project
project_id: "a1b2c3d4e5f6"
project_name: "my-react-app"
---

# Prefer Functional Style

## Action
Use functional patterns over classes when appropriate.

## Evidence
- Observed 5 instances of functional pattern preference
- User corrected class-based approach to functional on 2025-01-15
```

**属性：**
- **原子化** -- 一个 trigger，一个 action
- **置信度加权** -- 0.3 = 试探性，0.9 = 几乎确定
- **领域标记** -- code-style、testing、git、debugging、workflow 等
- **有证据支持** -- 追踪哪些观察创建了它
- **作用域感知** -- `project`（默认）或 `global`

## 工作原理

```
Session Activity (in a git repo)
      |
      | Hooks 捕获 prompt + 工具使用（100% 可靠）
      | + 检测项目上下文（git remote / repo path）
      v
+---------------------------------------------+
|  projects/<project-hash>/observations.jsonl  |
|   (prompts, tool calls, outcomes, project)   |
+---------------------------------------------+
      |
      | Observer agent 读取（后台，Haiku）
      v
+---------------------------------------------+
|          模式检测 (PATTERN DETECTION)        |
|   * 用户纠正 -> 生成 instinct               |
|   * 错误修复 -> 生成 instinct               |
|   * 重复工作流 -> 生成 instinct             |
|   * 作用域决策：project 还是 global？        |
+---------------------------------------------+
      |
      | 创建/更新
      v
+---------------------------------------------+
|  projects/<project-hash>/instincts/personal/ |
|   * prefer-functional.yaml (0.7) [project]   |
|   * use-react-hooks.yaml (0.9) [project]     |
+---------------------------------------------+
|  instincts/personal/  (全局 GLOBAL)          |
|   * always-validate-input.yaml (0.85) [global]|
|   * grep-before-edit.yaml (0.6) [global]     |
+---------------------------------------------+
      |
      | /evolve 聚类 + /promote 提升
      v
+---------------------------------------------+
|  projects/<hash>/evolved/ (项目作用域)       |
|  evolved/ (全局)                             |
|   * commands/new-feature.md                  |
|   * skills/testing-workflow.md               |
|   * agents/refactor-specialist.md            |
+---------------------------------------------+
```

## 项目检测

系统会自动检测你当前的项目：

1. **`CLAUDE_PROJECT_DIR` 环境变量**（最高优先级）
2. **`git remote get-url origin`** -- 哈希生成一个可移植的项目 ID（同一 repo 在不同机器上得到相同 ID）
3. **`git rev-parse --show-toplevel`** -- 回退方案，使用 repo 路径（机器相关）
4. **全局回退** -- 如果未检测到项目，本能归入全局作用域

每个项目会生成一个 12 字符的哈希 ID（如 `a1b2c3d4e5f6`）。注册文件 `~/.claude/homunculus/projects.json` 将 ID 映射为人类可读的名称。

## 快速开始

### 1. 启用观察 Hooks

**如果作为插件安装**（推荐）：

无需额外的 `settings.json` hook 配置。Claude Code v2.1+ 会自动加载插件 `hooks/hooks.json`，`observe.sh` 已在其中注册。

如果你之前将 `observe.sh` 复制到了 `~/.claude/settings.json`，请移除重复的 `PreToolUse` / `PostToolUse` 配置块。重复的插件 hook 会导致双重执行和 `${CLAUDE_PLUGIN_ROOT}` 解析错误，因为该变量仅在插件管理的 `hooks/hooks.json` 条目中可用。

**如果手动安装**到 `~/.claude/skills`，请将以下内容添加到你的 `~/.claude/settings.json`：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh"
      }]
    }]
  }
}
```

### 2. 初始化目录结构

系统会在首次使用时自动创建目录，你也可以手动创建：

```bash
# 全局目录
mkdir -p ~/.claude/homunculus/{instincts/{personal,inherited},evolved/{agents,skills,commands},projects}

# 项目目录会在 hook 首次在 git repo 中运行时自动创建
```

### 3. 使用本能命令

```bash
/instinct-status     # 显示已学到的本能（项目 + 全局）
/evolve              # 将相关的本能聚类为 skills/commands
/instinct-export     # 将本能导出到文件
/instinct-import     # 从他人处导入本能
/promote             # 将项目本能提升为全局作用域
/projects            # 列出所有已知项目及其本能数量
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `/instinct-status` | 显示所有本能（项目作用域 + 全局），含置信度 |
| `/evolve` | 将相关的本能聚类为 skills/commands，建议提升候选 |
| `/instinct-export` | 导出本能（可按作用域/领域过滤） |
| `/instinct-import <file>` | 导入本能，支持作用域控制 |
| `/promote [id]` | 将项目本能提升为全局作用域 |
| `/projects` | 列出所有已知项目及其本能数量 |

## 配置

编辑 `config.json` 来控制后台 observer：

```json
{
  "version": "2.1",
  "observer": {
    "enabled": false,
    "run_interval_minutes": 5,
    "min_observations_to_analyze": 20
  }
}
```

| 键 | 默认值 | 描述 |
|-----|---------|-------------|
| `observer.enabled` | `false` | 启用后台 observer agent |
| `observer.run_interval_minutes` | `5` | observer 分析观察数据的频率 |
| `observer.min_observations_to_analyze` | `20` | 开始分析前的最小观察数 |

其他行为（观察捕获、本能阈值、项目作用域、提升标准）通过 `instinct-cli.py` 和 `observe.sh` 中的代码默认值配置。

## 文件结构

```
~/.claude/homunculus/
+-- identity.json           # 你的个人资料、技术水平
+-- projects.json           # 注册表：project hash -> name/path/remote
+-- observations.jsonl      # 全局观察数据（回退方案）
+-- instincts/
|   +-- personal/           # 全局自动学习的本能
|   +-- inherited/          # 全局导入的本能
+-- evolved/
|   +-- agents/             # 全局生成的 agents
|   +-- skills/             # 全局生成的 skills
|   +-- commands/           # 全局生成的 commands
+-- projects/
    +-- a1b2c3d4e5f6/       # 项目哈希（来自 git remote URL）
    |   +-- project.json    # 每个项目的元数据镜像 (id/name/root/remote)
    |   +-- observations.jsonl
    |   +-- observations.archive/
    |   +-- instincts/
    |   |   +-- personal/   # 项目特定的自动学习
    |   |   +-- inherited/  # 项目特定的导入
    |   +-- evolved/
    |       +-- skills/
    |       +-- commands/
    |       +-- agents/
    +-- f6e5d4c3b2a1/       # 另一个项目
        +-- ...
```

## 作用域决策指南

| 模式类型 | 作用域 | 示例 |
|-------------|-------|---------|
| 语言/框架约定 | **project** | "Use React hooks"、"Follow Django REST patterns" |
| 文件结构偏好 | **project** | "测试放在 `__tests__`/"、"组件放在 src/components/" |
| 代码风格 | **project** | "使用函数式风格"、"优先使用 dataclasses" |
| 错误处理策略 | **project** | "使用 Result 类型处理错误" |
| 安全实践 | **global** | "验证用户输入"、"净化 SQL" |
| 通用最佳实践 | **global** | "先写测试"、"始终处理错误" |
| 工具工作流偏好 | **global** | "先 Grep 再 Edit"、"先 Read 再 Write" |
| Git 实践 | **global** | "Conventional commits"、"小而有重点的提交" |

## 本能提升（项目 -> 全局）

当同一个本能在多个项目中以高置信度出现时，它就可以被提升为全局作用域。

**自动提升标准：**
- 相同 instinct ID 出现在 2+ 项目中
- 平均置信度 >= 0.8

**如何提升：**

```bash
# 提升特定的本能
python3 instinct-cli.py promote prefer-explicit-errors

# 自动提升所有符合条件的本能
python3 instinct-cli.py promote

# 预览（不实际执行）
python3 instinct-cli.py promote --dry-run
```

`/evolve` 命令也会建议提升候选。

## 置信度评分

置信度随时间演变：

| 分数 | 含义 | 行为 |
|-------|---------|----------|
| 0.3 | 试探性 | 建议但不强制 |
| 0.5 | 中等 | 相关时应用 |
| 0.7 | 强 | 自动批准应用 |
| 0.9 | 几乎确定 | 核心行为 |

**置信度增加** 当：
- 模式被重复观察到
- 用户没有纠正建议的行为
- 来自其他来源的相似本能一致

**置信度降低** 当：
- 用户明确纠正了行为
- 长时间未观察到该模式
- 出现矛盾证据

## 为什么使用 Hooks 而非 Skills 进行观察

> "v1 依赖 skills 进行观察。Skills 是概率性的——它们基于 Claude 的判断，大约 50-80% 的时间会触发。"

Hooks **100% 确定性地**触发。这意味着：
- 每个工具调用都被观察
- 没有模式被遗漏
- 学习是全面的

## 向后兼容

v2.1 完全兼容 v2.0 和 v1：
- `~/.claude/homunculus/instincts/` 中已有的全局本能仍然作为全局本能工作
- v1 中 `~/.claude/skills/learned/` 已有的 skills 仍然有效
- Stop hook 仍然运行（但同时也将数据输入 v2）
- 渐进迁移：可以两者并行运行

## 隐私

- 观察数据**保留在本地**机器上
- 项目作用域的本能在每个项目中隔离
- 只有**本能（模式）**可以被导出——原始观察数据不行
- 不会共享实际代码或对话内容
- 你可以控制哪些内容被导出和提升

## 相关资源

- [ECC-Tools GitHub App](https://github.com/apps/ecc-tools) - 从仓库历史生成本能
- Homunculus - 启发了 v2 本能架构的社区项目（原子观察、置信度评分、本能演化流水线）
- [长篇指南](https://x.com/affaanmustafa/status/2014040193557471352) - 持续学习章节

---

*基于本能的学习：一次一个项目，教会 Claude 你的模式。*
