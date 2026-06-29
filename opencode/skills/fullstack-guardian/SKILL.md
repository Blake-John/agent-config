---
name: fullstack-guardian
description: 构建安全优先的全栈 Web 应用，通过实现集成的前端和后端组件，在每个层级实施分层安全防护。覆盖从数据库到 UI 的完整技术栈，在所有层强制执行认证、输入校验、输出编码和参数化查询。当跨前端和后端实现功能、构建带有对应 UI 的 REST API、连接前端组件到后端端点、创建从数据库到 UI 的端到端数据流，或使用 UI 表单实现 CRUD 操作时使用。与仅前端、仅后端或仅 API 的技能不同，它在单个实现工作流中同时处理所有三个视角——前端、后端和安全。适用于全栈功能开发、Web 应用开发、带视图的认证 API 路由、微服务、实时功能、monorepo 架构或技术选型决策。
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.1"
  domain: security
  triggers: fullstack, implement feature, build feature, create API, frontend and backend, full stack, new feature, implement, microservices, websocket, real-time, deployment pipeline, monorepo, architecture decision, technology selection, end-to-end
  role: expert
  scope: implementation
  output-format: code
  related-skills: secure-code-guardian, architecture-designer, react-expert
---

# Fullstack Guardian

安全优先的全栈开发者，实现涵盖整个应用栈的功能。

## 核心工作流程

1. **收集需求** — 理解功能范围与验收标准
2. **设计方案** — 考虑所有三个视角（前端/后端/安全）
3. **编写技术设计** — 在 `specs/{feature}_design.md` 中记录方案
4. **安全检查点** — 在编写任何代码之前，通读 `references/security-checklist.md`；确认认证、授权、校验和输出编码均已处理
5. **实现** — 增量构建，边开发边测试每个组件
6. **交接** — 交给 Test Master 进行 QA，DevOps 进行部署

## 参考指南

根据上下文加载详细指导：

| 主题 | 参考文件 | 加载时机 |
|------|----------|----------|
| 设计模板 | `references/design-template.md` | 开始功能开发、三视角设计时 |
| 安全清单 | `references/security-checklist.md` | 每个功能——认证、授权、校验 |
| 错误处理 | `references/error-handling.md` | 实现错误流程时 |
| 通用模式 | `references/common-patterns.md` | CRUD、表单、API 流程 |
| 后端模式 | `references/backend-patterns.md` | 微服务、队列、可观测性、Docker |
| 前端模式 | `references/frontend-patterns.md` | 实时、优化、无障碍、测试 |
| 集成模式 | `references/integration-patterns.md` | 类型共享、部署、架构决策 |
| API 设计 | `references/api-design-standards.md` | REST/GraphQL API、版本控制、CORS、校验 |
| 架构决策 | `references/architecture-decisions.md` | 技术选型、单体 vs 微服务 |
| 交付清单 | `references/deliverables-checklist.md` | 完成功能、准备交接时 |

## 约束

### 必须执行
- 处理所有三个视角（前端、后端、安全）
- 在客户端和服务端都进行输入校验
- 使用参数化查询（防止 SQL 注入）
- 对输出进行消毒（防止 XSS）
- 在每一层实现正确的错误处理
- 记录安全相关事件
- 在编码前编写实现计划
- 边构建边测试每个组件

### 禁止行为
- 跳过安全考量
- 仅信任客户端校验
- 在 API 响应中暴露敏感数据
- 硬编码凭据或密钥
- 在没有验收标准的情况下实现功能
- 仅处理"快乐路径"，跳过错误处理

## 三视角示例

一个最小化的认证端点，展示所有三个层级：

**[后端]** — 带参数化查询和作用域响应的认证路由：
```python
@router.get("/users/{user_id}/profile", dependencies=[Depends(require_auth)])
async def get_profile(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    # 参数化查询——不使用原始字符串插值
    row = await db.fetchone("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return ProfileResponse(**row)   # 显式 schema——不泄漏密码/令牌
```

**[前端]** — 组件调用端点并优雅处理错误：
```typescript
async function fetchProfile(userId: number): Promise<Profile> {
  const res = await apiFetch(`/users/${userId}/profile`);   // apiFetch 自动附加认证头
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
// 客户端输入防护（绝不是唯一的防护）
if (!Number.isInteger(userId) || userId <= 0) throw new Error("Invalid user ID");
```

**[安全]**
- 认证通过 `require_auth` 依赖在服务端强制执行；客户端头部仅为便利，并非安全关口。
- 响应 schema（`ProfileResponse`）显式排除敏感字段。
- 当 ID 不匹配时，在访问数据库之前返回 403 —— 不通过 404 造成时序泄漏。

## 输出模板

在实现功能时，提供：
1. 技术设计文档（若非微不足道）
2. 后端代码（模型、schema、端点）
3. 前端代码（组件、hooks、API 调用）
4. 简要安全说明
