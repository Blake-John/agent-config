---
name: codegraph
description: 预索引的代码知识图谱工具，支持 20+ 编程语言，100% 本地运行。用于快速探索项目、查找目标内容、分析依赖关系。一次调用返回相关符号的源代码、调用路径和爆炸半径摘要。触发词：探索项目、查找代码、分析依赖、影响分析、代码搜索、项目结构。
license: MIT
metadata:
  author: colbymchenry
  version: "1.0.0"
  domain: code-analysis
  triggers: 代码搜索, 项目探索, 依赖分析, 影响分析, 代码导航, code search, explore project, dependency analysis, impact analysis
  role: specialist
  scope: analysis
  output-format: structured
  related-skills: codebase-onboarding, code-reviewer, refactor-cleaner
  languages: TypeScript, JavaScript, Python, Go, Rust, Java, C#, PHP, Ruby, C, C++, Swift, Kotlin, Scala, Dart, Lua, R, Svelte, Vue, Astro
  tools: CLI, MCP
  requires-installation: true
  auto-sync: true
  local-only: true
---

# CodeGraph Skill

预索引的代码知识图谱工具，支持 20+ 编程语言，100% 本地运行。

## 概述

CodeGraph 是一个预构建的代码知识图谱工具，可以：
- 预索引代码知识图谱，在代码更改时自动同步
- 一次调用返回相关符号的源代码、调用路径和爆炸半径摘要
- 支持 20+ 编程语言
- 100% 本地运行，不需要外部服务
- 自动同步，无需手动运行

## 安装

### 1. 安装 CLI

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh

# Windows (PowerShell)
irm https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.ps1 | iex

# 或者使用 npm
npm i -g @colbymchenry/codegraph
```

### 2. 连接 Agent

```bash
codegraph install
```

### 3. 初始化项目

```bash
cd your-project
codegraph init
```

## 核心能力

### 1. 项目结构探索

使用 `files` 命令扫描项目目录结构，识别关键目录和文件。

```bash
codegraph files [path]
```

**输出示例**：
```
project/
├── src/
│   ├── app/          # Next.js App Router
│   ├── components/   # React 组件
│   └── lib/          # 工具库
├── public/           # 静态资源
├── package.json      # 项目配置
└── tsconfig.json     # TypeScript 配置
```

### 2. 代码搜索

使用 `query` 命令搜索特定代码模式、函数、类、变量。

```bash
codegraph query <search>
```

**示例**：
```bash
# 搜索 login 函数
codegraph query "login"

# 搜索 User 类
codegraph query "User"

# 搜索认证相关代码
codegraph query "auth"
```

### 3. 依赖分析

使用 `callers` 和 `callees` 命令分析依赖关系。

```bash
# 查找调用者
codegraph callers <symbol>

# 查找被调用者
codegraph callees <symbol>
```

**示例**：
```bash
# 查找谁调用了 login 函数
codegraph callers login

# 查找 login 函数调用了什么
codegraph callees login
```

### 4. 功能定位

使用 `explore` 命令定位特定功能的实现位置。

```bash
codegraph explore <query>
```

**示例**：
```bash
# 探索登录功能
codegraph explore "用户登录功能"

# 探索认证流程
codegraph explore "认证流程"

# 探索数据库操作
codegraph explore "数据库操作"
```

### 5. 影响分析

使用 `impact` 命令分析变更的影响范围。

```bash
codegraph impact <symbol>
```

**示例**：
```bash
# 分析修改 login 函数的影响范围
codegraph impact login

# 分析修改 User 类的影响范围
codegraph impact User
```

### 6. 符号节点

使用 `node` 命令获取符号的源代码和调用者。

```bash
codegraph node <symbol|file>
```

**示例**：
```bash
# 获取 login 函数的源代码
codegraph node login

# 获取文件内容
codegraph node src/lib/auth.ts
```

## MCP 工具

当 CodeGraph 作为 MCP 服务器运行时，暴露一个工具：

### codegraph_explore

一次调用获取符号源代码、调用路径、爆炸半径。

**使用场景**：
- "how does X work" - 了解某个功能如何工作
- "how does X reach Y" - 追踪调用路径
- 调查某个区域
- 阅读某个符号或文件的源代码

**返回内容**：
- 相关符号的源代码（按文件分组）
- 符号之间的调用路径
- 爆炸半径摘要

**示例**：
```bash
# 了解登录功能如何工作
codegraph explore "用户登录功能"

# 追踪认证流程
codegraph explore "认证流程如何到达数据库"

# 阅读特定文件
codegraph explore "src/lib/auth.ts"
```

## 调用方式

### CLI 为主

优先使用 CLI 命令调用 codegraph，当 CLI 不可用时使用 MCP。

### MCP 为备选

当 CLI 不可用时，使用 MCP 工具调用 codegraph。

## 使用场景

### 场景 1: 了解项目结构

```bash
# 使用 CLI
codegraph files

# 使用 MCP
codegraph_explore "项目结构"
```

### 场景 2: 查找特定功能

```bash
# 使用 CLI
codegraph query "login"
codegraph explore "登录功能"

# 使用 MCP
codegraph_explore "登录功能"
```

### 场景 3: 分析依赖关系

```bash
# 使用 CLI
codegraph callers login
codegraph callees login

# 使用 MCP
codegraph_explore "login 函数的调用关系"
```

### 场景 4: 影响分析

```bash
# 使用 CLI
codegraph impact login

# 使用 MCP
codegraph_explore "修改 login 函数的影响范围"
```

## 最佳实践

1. **优先使用 CLI** - CLI 命令更直接，易于调试和组合
2. **使用 explore 命令** - explore 命令返回最完整的信息
3. **结合 CLI 和 MCP** - 根据场景选择合适的调用方式
4. **利用自动同步** - CodeGraph 会自动同步代码更改，无需手动更新
5. **使用具体查询** - 查询越具体，返回的结果越精确

## 常见问题

### Q: CodeGraph 支持哪些语言？

A: 支持 20+ 语言，包括 TypeScript, JavaScript, Python, Go, Rust, Java, C#, PHP, Ruby, C, C++, Swift, Kotlin, Scala, Dart, Lua, Luau, R, Svelte, Vue, Astro, Liquid, Pascal/Delphi。

### Q: CodeGraph 需要外部服务吗？

A: 不需要，100% 本地运行，使用 SQLite 数据库。

### Q: 如何更新 CodeGraph？

A: 运行 `codegraph upgrade` 命令。

### Q: 如何卸载 CodeGraph？

A: 运行 `codegraph uninstall` 命令。

## 相关链接

- [GitHub 仓库](https://github.com/colbymchenry/codegraph)
- [文档](https://colbymchenry.github.io/codegraph/)
- [npm 包](https://www.npmjs.com/package/@colbymchenry/codegraph)
