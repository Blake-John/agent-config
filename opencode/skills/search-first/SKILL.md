---
name: search-first
description: 研究先于编码的工作流。在编写自定义代码之前搜索现有的工具、库和模式。
---

# /search-first — 研究先于编码

系统化"在实现之前搜索现有解决方案"的工作流程。

## 触发条件

在以下情况使用此技能：

- 开始一个新功能，可能存在现有解决方案
- 添加依赖或集成
- 用户要求"添加 X 功能"且你正准备编写代码
- 在创建新的工具函数、辅助函数或抽象之前

## 工作流程

```
┌─────────────────────────────────────────────┐
│  1. NEED ANALYSIS                           │
│     Define what functionality is needed      │
│     Identify language/framework constraints  │
├─────────────────────────────────────────────┤
│  2. PARALLEL SEARCH                        │
│     ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│     │  npm /   │ │  MCP /   │ │  GitHub / │  │
│     │  PyPI    │ │  Skills  │ │  Web      │  │
│     └──────────┘ └──────────┘ └──────────┘  │
├─────────────────────────────────────────────┤
│  3. EVALUATE                                │
│     Score candidates (functionality, maint, │
│     community, docs, license, deps)         │
├─────────────────────────────────────────────┤
│  4. DECIDE                                  │
│     ┌─────────┐  ┌──────────┐  ┌─────────┐  │
│     │  Adopt  │  │  Extend  │  │  Build   │  │
│     │ as-is   │  │  /Wrap   │  │  Custom  │  │
│     └─────────┘  └──────────┘  └─────────┘  │
├─────────────────────────────────────────────┤
│  5. IMPLEMENT                               │
│     Install package / Configure MCP /       │
│     Write minimal custom code               │
└─────────────────────────────────────────────┘
```

## 决策矩阵

| 信号 | 行动 |
|--------|--------|
| 完全匹配、维护良好、MIT/Apache 许可 | **采用** — 直接安装使用 |
| 部分匹配、基础良好 | **扩展** — 安装 + 编写薄封装层 |
| 多个弱匹配 | **组合** — 组合 2-3 个小包 |
| 未找到合适方案 | **自建** — 编写自定义代码，但参考研究结果 |

## 使用方法

### 快速模式（内联）

在编写工具函数或添加功能之前，快速思考以下问题：

0. 仓库中是否已存在？→ 先用 `rg` 搜索相关模块/测试
1. 是否是常见问题？→ 搜索 npm/PyPI
2. 是否有对应的 MCP？→ 检查配置文件并搜索
3. 是否有对应的技能？→ 检查技能文件
4. 是否有 GitHub 实现/模板？→ 在编写全新代码之前，先运行 GitHub 代码搜索找维护良好的 OSS

### 完整模式

对于非 trivial 功能，先委托研究来识别现有工具，然后再实现：

```
研究内容：[要查找的工具/库的描述]
语言/框架：[编程语言或框架]
约束条件：[任何限制条件]
搜索范围：npm/PyPI、MCP 服务器、GitHub
输出：结构化对比分析及推荐
```

## 按类别的搜索快捷方式

### 开发工具

- 代码检查 → `eslint`, `ruff`, `textlint`, `markdownlint`
- 格式化 → `prettier`, `black`, `gofmt`
- 测试 → `jest`, `pytest`, `go test`
- 预提交 → `husky`, `lint-staged`, `pre-commit`

### AI/LLM 集成

- Claude SDK → 使用 Context7 获取最新文档
- Prompt 管理 → 检查 MCP 服务器
- 文档处理 → `unstructured`, `pdfplumber`, `mammoth`

### 数据与 API

- HTTP 客户端 → `httpx` (Python), `ky`/`got` (Node)
- 数据验证 → `zod` (TS), `pydantic` (Python)
- 数据库 → 先检查 MCP 服务器

### 内容与发布

- Markdown 处理 → `remark`, `unified`, `markdown-it`
- 图片优化 → `sharp`, `imagemin`

## 集成点

### 与规划工作流集成

研究应在阶段 1（架构审查）之前完成：

- 识别可用工具
- 将发现纳入实现计划
- 避免"重复造轮子"

### 与架构设计集成

将研究发现用于：

- 技术栈决策
- 集成模式发现
- 现有参考架构

### 与迭代检索技能集成

结合使用以实现渐进式发现：

- 循环 1：广泛搜索（npm, PyPI, MCP）
- 循环 2：详细评估最候选方案
- 循环 3：测试与项目约束的兼容性

## 示例

### 示例 1："添加死链检查"

```
Need: Check markdown files for broken links
Search: npm "markdown dead link checker"
Found: textlint-rule-no-dead-link (score: 9/10)
Action: ADOPT — npm install textlint-rule-no-dead-link
Result: Zero custom code, battle-tested solution
```

### 示例 2："添加 HTTP 客户端封装"

```
Need: Resilient HTTP client with retries and timeout handling
Search: npm "http client retry", PyPI "httpx retry"
Found: got (Node) with retry plugin, httpx (Python) with built-in retry
Action: ADOPT — use got/httpx directly with retry config
Result: Zero custom code, production-proven libraries
```

### 示例 3："添加配置文件检查工具"

```
Need: Validate project config files against a schema
Search: npm "config linter schema", "json schema validator cli"
Found: ajv-cli (score: 8/10)
Action: ADOPT + EXTEND — install ajv-cli, write project-specific schema
Result: 1 package + 1 schema file, no custom validation logic
```

## 反模式

- **直接上手编码**：未检查是否已有现成工具函数就开始编写
- **忽略 MCP**：未检查 MCP 服务器是否已提供所需能力
- **过度定制**：过度封装库以至于失去其优势
- **依赖膨胀**：为一个小功能安装庞大的包
