---
description: 从 git 历史分析生成 skill
agent: build
---

# Skill 创建命令

分析 git 历史生成 skill：$ARGUMENTS

## 分析流程

### 步骤 1：收集提交数据
```bash
git log --oneline -100                              # 最近提交
git log --name-only --pretty=format: | sort | uniq -c | sort -rn  # 按文件类型
git log --pretty=format: --name-only | sort | uniq -c | sort -rn | head -20  # 最常变更的文件
```

### 步骤 2：识别模式

**提交信息模式**：
- 常用前缀（feat、fix、refactor）
- 命名约定
- 合作者模式

**代码模式**：
- 文件结构约定
- 导入组织方式
- 错误处理方法

### 步骤 3：生成 SKILL.md

```markdown
# [Skill 名称]

## 概述
[此 skill 教授什么]

## 模式

### 模式 1：[名称]
- 何时使用
- 实现
- 示例

## 最佳实践
1. [实践 1]
2. [实践 2]

## 常见错误
1. [错误 1] — 如何避免
```

## 输出

创建：
- `skills/[name]/SKILL.md` — Skill 文档
- `skills/[name]/instincts.json` — Instinct 集合

---

**提示**：运行 `/skill-create --instincts` 以同时生成 instinct。
