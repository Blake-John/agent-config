---
name: codebase-onboarding
description: 快速分析不熟悉的代码库，生成结构化的入门指南和 AGENTS.md。使用 codegraph 进行代码分析，支持项目侦察、架构映射、约定检测。触发词：入门项目、理解代码库、生成 AGENTS.md、onboard me、walk me through。
license: MIT
metadata:
  author: ECC
  version: "2.0.0"
  domain: onboarding
  triggers: 入门, 理解代码库, 生成 AGENTS.md, onboard, walk me through, 项目结构, 新项目, 加入团队
  role: specialist
  scope: documentation
  output-format: markdown
  related-skills: codegraph, code-reviewer, architecture-designer
  requires: codegraph
  languages: all
  tools: CLI
  requires-installation: false
  auto-sync: false
  local-only: true
---

# 代码库入门

快速分析不熟悉的代码库，生成结构化的入门指南。

## 使用场景

- 第一次打开项目
- 加入新团队或仓库
- 生成 AGENTS.md
- 用户说"onboard me"或"walk me through this repo"

## 依赖

本 skill 依赖 codegraph skill 进行代码分析。请确保：

1. 已安装 codegraph CLI
2. 已初始化项目（`codegraph init`）
3. 已加载 codegraph skill

## 工作流程

### 阶段 1: 项目侦察

使用 codegraph 快速获取项目信息：

```bash
# 获取项目结构
codegraph files

# 搜索关键文件
codegraph query "package.json"
codegraph query "tsconfig.json"
codegraph query "README.md"

# 搜索入口点
codegraph query "main"
codegraph query "index"
codegraph query "app"
```

### 阶段 2: 架构映射

使用 codegraph 分析架构：

```bash
# 分析依赖关系
codegraph callers <symbol>
codegraph callees <symbol>

# 分析影响范围
codegraph impact <symbol>

# 探索特定功能
codegraph explore "authentication"
codegraph explore "database"
codegraph explore "api"
```

### 阶段 3: 约定检测

使用 codegraph 检测代码约定：

```bash
# 搜索命名模式
codegraph query "class"
codegraph query "function"
codegraph query "interface"

# 搜索错误处理
codegraph query "try"
codegraph query "catch"
codegraph query "throw"

# 搜索测试模式
codegraph query "test"
codegraph query "spec"
codegraph query "describe"
```

### 阶段 4: 生成入门文档

基于侦察数据，生成：

1. **入门指南** - 项目概述、技术栈、架构、关键目录
2. **AGENTS.md** - 项目特定的指令

## 输出格式

### 入门指南

```markdown
# 入门指南: [项目名称]

## 概述
[项目简介]

## 技术栈
| 层级 | 技术 | 版本 |
|------|------|------|
| 语言 | TypeScript | 5.x |
| 框架 | Next.js | 14.x |
| 数据库 | PostgreSQL | 16 |

## 架构
[架构描述]

## 关键入口点
- API 路由: `src/app/api/`
- UI 页面: `src/app/(dashboard)/`
- 数据库: `prisma/schema.prisma`

## 目录映射
[目录 → 用途]

## 请求生命周期
[请求从入口到响应的流程]

## 约定
- [文件命名模式]
- [错误处理方式]
- [测试模式]
- [Git 工作流]

## 常用命令
- 运行开发服务器: `npm run dev`
- 运行测试: `npm test`
- 运行 lint: `npm run lint`

## 去哪里找
| 我想... | 看... |
|---------|-------|
| 添加 API 端点 | `src/app/api/` |
| 添加 UI 页面 | `src/app/(dashboard)/` |
| 添加数据库表 | `prisma/schema.prisma` |
| 添加测试 | `tests/` |
```

### AGENTS.md

```markdown
# 项目指令

## 技术栈
[检测到的技术栈摘要]

## 代码风格
- [检测到的命名约定]
- [检测到的模式]

## 测试
- 运行测试: `[检测到的测试命令]`
- 测试模式: [检测到的测试文件约定]
- 覆盖率: [如果配置了，覆盖率命令]

## 构建和运行
- 开发: `[检测到的开发命令]`
- 构建: `[检测到的构建命令]`
- Lint: `[检测到的 lint 命令]`

## 项目结构
[关键目录 → 用途映射]

## 约定
- [提交风格]
- [PR 工作流]
- [错误处理模式]
```

## 最佳实践

1. **不要读取所有文件** - 侦察阶段使用 codegraph，不要读取每个文件
2. **验证，不要猜测** - 如果从配置检测到框架但实际代码使用不同的东西，以代码为准
3. **尊重现有的 AGENTS.md** - 如果已存在，增强它而不是替换它
4. **保持简洁** - 入门指南应该能在 2 分钟内浏览完
5. **标记未知** - 如果无法确定某个约定，说出来而不是猜测

## 反模式

- 生成超过 100 行的 AGENTS.md - 保持聚焦
- 列出每个依赖 - 只突出影响代码编写方式的依赖
- 描述明显的目录名 - `src/` 不需要解释
- 复制 README - 入门指南添加 README 缺少的结构洞察

## 示例

### 示例 1: 第一次进入新仓库

**用户**: "Onboard me to this codebase"
**操作**: 运行完整的 4 阶段工作流 → 生成入门指南 + AGENTS.md
**输出**: 入门指南直接打印到对话中，AGENTS.md 写入项目根目录

### 示例 2: 为现有项目生成 AGENTS.md

**用户**: "Generate an AGENTS.md for this project"
**操作**: 运行阶段 1-3，跳过入门指南，只生成 AGENTS.md
**输出**: 项目特定的 `AGENTS.md`

### 示例 3: 增强现有的 AGENTS.md

**用户**: "Update the AGENTS.md with current project conventions"
**操作**: 读取现有的 AGENTS.md，运行阶段 1-3，合并新发现
**输出**: 更新后的 `AGENTS.md`，新增内容明确标记
