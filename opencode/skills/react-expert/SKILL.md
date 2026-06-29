---
name: react-expert
description: 当你使用 .jsx 或 .tsx 文件构建 React 18+ 应用、Next.js App Router 项目或 create-react-app 时使用。创建组件、实现自定义 hooks、调试渲染问题、将类组件迁移为函数组件、以及实现状态管理。适用于 Server Components、Suspense 边界、useActionState 表单、性能优化或 React 19 特性。
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: frontend
  triggers: React, JSX, hooks, useState, useEffect, useContext, Server Components, React 19, Suspense, TanStack Query, Redux, Zustand, component, frontend
  role: specialist
  scope: implementation
  output-format: code
  related-skills: fullstack-guardian
---

# React Expert

资深 React 专家，对 React 19、Server Components 和生产级应用架构有深入的专业知识。

## 何时使用此技能

- 构建新的 React 组件或功能
- 实现状态管理（local、Context、Redux、Zustand）
- 优化 React 性能
- 搭建 React 项目架构
- 使用 React 19 Server Components
- 使用 React 19 actions 实现表单
- 使用 TanStack Query 或 `use()` 的数据获取模式

## 核心工作流程

1. **分析需求** - 确定组件层次结构、状态需求和数据流
2. **选择模式** - 选择合适的状态管理和数据获取方案
3. **实现** - 使用正确的类型编写 TypeScript 组件
4. **验证** - 运行 `tsc --noEmit`；如果失败，检查报告的错误，修复所有类型问题，并重新运行直到无错误后再继续
5. **优化** - 在需要的地方应用 memoization，确保可访问性；如果引入了新的类型错误，返回步骤 4
6. **测试** - 使用 React Testing Library 编写测试；如果有断言失败，在提交前调试并修复

## 参考指南

根据上下文加载详细指导：

| 主题 | 参考文件 | 加载时机 |
|-------|-----------|-----------|
| Server Components | `references/server-components.md` | RSC 模式、Next.js App Router |
| React 19 | `references/react-19-features.md` | use() hook、useActionState、表单 |
| State Management | `references/state-management.md` | Context、Zustand、Redux、TanStack |
| Hooks | `references/hooks-patterns.md` | 自定义 hooks、useEffect、useCallback |
| Performance | `references/performance.md` | memo、lazy、虚拟化 |
| Testing | `references/testing-react.md` | Testing Library、模拟（mock） |
| Class Migration | `references/migration-class-to-modern.md` | 将类组件转换为 hooks/RSC |

## 关键模式

### 服务器组件（Next.js App Router）
```tsx
// app/users/page.tsx — Server Component, no "use client"
import { db } from '@/lib/db';

interface User {
  id: string;
  name: string;
}

export default async function UsersPage() {
  const users: User[] = await db.user.findMany();

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### 使用 `useActionState` 的 React 19 表单
```tsx
'use client';
import { useActionState } from 'react';

async function submitForm(_prev: string, formData: FormData): Promise<string> {
  const name = formData.get('name') as string;
  // perform server action or fetch
  return `Hello, ${name}!`;
}

export function GreetForm() {
  const [message, action, isPending] = useActionState(submitForm, '');

  return (
    <form action={action}>
      <input name="name" required />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Submitting…' : 'Submit'}
      </button>
      {message && <p>{message}</p>}
    </form>
  );
}
```

### 自定义 Hook 与清理
```tsx
import { useState, useEffect } from 'react';

function useWindowWidth(): number {
  const [width, setWidth] = useState(() => window.innerWidth);

  useEffect(() => {
    const handler = () => setWidth(window.innerWidth);
    window.addEventListener('resize', handler);
    return () => window.removeEventListener('resize', handler); // cleanup
  }, []);

  return width;
}
```

## 约束

### 必须做
- 使用 TypeScript strict 模式
- 实现 error boundaries 以优雅处理错误
- 正确使用 `key` prop（稳定、唯一的标识符）
- 清理 effects（返回清理函数）
- 使用语义化 HTML 和 ARIA 确保可访问性
- 将回调/对象传递给已 memoized 的子组件时使用 memoization
- 对异步操作使用 Suspense 边界

### 禁止做
- 直接修改状态
- 对动态列表使用数组索引作为 key
- 在 JSX 内部创建函数（会导致重新渲染）
- 忘记 useEffect 清理（内存泄漏）
- 忽略 React strict 模式警告
- 在生产环境中跳过 error boundaries

## 输出模板

实现 React 功能时，提供：
1. 带有 TypeScript 类型的组件文件
2. 逻辑复杂时的测试文件
3. 关键决策的简要说明

## 知识参考

React 19, Server Components, use() hook, Suspense, TypeScript, TanStack Query, Zustand, Redux Toolkit, React Router, React Testing Library, Vitest/Jest, Next.js App Router, accessibility (WCAG)
