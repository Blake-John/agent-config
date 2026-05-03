---
name: dev-workflow
description: 项目开发工作流程。指导新功能和 bug 修复的完整实现流程，包括研究、设计、实现、测试、审查和提交六个阶段。适用于需要按照标准流程进行开发的任务。需要和 agent-engine 结合使用。
---

# Development Workflow Skill

## Overview

This workflow guides the whole project development, providing a comprehensive framework to ensure the development to be nice.

It should work with `agent-engine` skill for a more detailed control of development process.

## When to Use This Skill

Use this skill when:

- Implementing new features for the Rust Todo application
- Fixing bugs in the project
- User explicitly requests to follow the development workflow
- Starting any significant code change that requires structured approach

## Feature Implementation Flow

```
Research → Design → Implement → Test → Review → Commit
```

## Phase 1: Research

Use the proper agent and skills to start a research task.

### Step 1.1 - Codebase Research

- Read existing code in relevant modules
- Check similar patterns in codebase
- Document current behavior and data structures

### Step 1.2 - External Research (Required)

- Launch **deep-researcher** subagent to search for:
  - Existing Rust libraries for the feature
  - Open-source implementations (GitHub)
  - Best practices from crates.io
- Filter and summarize findings
- Report: "Useful because..." for each finding

### Step 1.3 - Requirement Clarification

- Verify feature scope with user if unclear
- Confirm edge cases
- Ask: "For this feature, I understand X. Is this correct?"

---

## Phase 2: Design

Use the proper agent and skills to start a design task.

### Step 2.1 - Framework Design

- Design the project architecture and tech stack
- Outline the implementation structure
- Identify files and functions to modify
- Define interfaces between modules

### Step 2.2 - Framework Review

- Present design to user
- Verify design matches feature requirements
- Adjust based on feedback

### Step 2.3 - Checklist

- [ ] New data structures defined
- [ ] New functions outlined
- [ ] Existing code to modify identified
- [ ] Edge cases considered

---

## Phase 3: Implement

Use the proper agent and skills to start a implementation task.

See the FEATIMPL instructions.

---

## Phase 4: Test

Use the proper agent and skills to start a test task.

---

## Phase 5: Review

Use the proper agent and skills to start a review task.

### Step 5.1 - Code Review

- Launch **code-reviewer** subagent
- Address CRITICAL/HIGH issues
- Fix MEDIUM issues when possible

### Step 5.2 - Quality Check

- [ ] No new warnings
- [ ] No hardcoded values
- [ ] Comments accurate
- [ ] README updated if needed

---

## Phase 6: Commit

### Commit Message Format

```
<type>: <description>

<optional body>
```

Types: feat, fix, refactor, docs, test, chore, polish

**Example**:

```
feat: implement sort mode with date/urgency options

- Add SortMode to CurrentMode enum
- Sort tasks by due date (asc/desc)
- Sort tasks by urgency (asc/desc)
- Allow manual reorder after sort
```
