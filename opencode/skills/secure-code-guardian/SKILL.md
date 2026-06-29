---
name: secure-code-guardian
description: 用于实现认证/授权、保护用户输入或防御 OWASP Top 10 漏洞 —— 包括自定义安全实现，例如使用 bcrypt/argon2 哈希密码、使用参数化语句清理 SQL 查询、配置 CORS/CSP 头部、使用 Zod 验证输入以及设置 JWT token。适用于认证、授权、输入验证、加密、OWASP Top 10 防护、安全会话管理和安全加固。对于预构建的 OAuth/SSO 集成或独立的安全审计，请考虑使用更专业的 skill。
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: security
  triggers: security, authentication, authorization, encryption, OWASP, vulnerability, secure coding, password, JWT, OAuth
  role: specialist
  scope: implementation
  output-format: code
  related-skills: fullstack-guardian, security-reviewer, architecture-designer
---

# Secure Code Guardian

## 核心工作流程

1. **威胁建模** —— 识别攻击面和威胁
2. **设计** —— 规划安全控制措施
3. **实现** —— 编写具有纵深防御的 safe 代码；参见下方代码示例
4. **验证** —— 使用明确的检查点（见下方）测试安全控制措施
5. **记录** —— 记录安全决策

### 验证检查点

每个实现步骤完成后，验证：

- **认证**：测试暴力破解防护（锁定/限速触发）、会话固定抵抗、token 过期和无效凭证错误消息（不得泄露用户是否存在）。
- **授权**：验证水平和垂直越权路径已被阻止；使用不同角色/用户的 token 进行测试。
- **输入处理**：确认 SQL 注入 payload（`' OR 1=1--`）被拒绝；确认 XSS payload（`<script>alert(1)</script>`）被转义或拒绝。
- **头部/CORS**：使用安全扫描器（例如 `curl -I`、Mozilla Observatory）验证安全头部已设置且 CORS 来源白名单正确。

## 参考指南

根据上下文加载详细指导：

| 主题 | 参考文件 | 加载时机 |
|-------|-----------|-----------|
| OWASP | `references/owasp-prevention.md` | OWASP Top 10 模式 |
| 认证 | `references/authentication.md` | 密码哈希、JWT |
| 输入验证 | `references/input-validation.md` | Zod、SQL 注入 |
| XSS/CSRF | `references/xss-csrf.md` | XSS 防护、CSRF |
| 头部 | `references/security-headers.md` | Helmet、限流 |

## 约束条件

### 必须执行
- 使用 bcrypt/argon2 哈希密码（绝不使用 MD5/SHA-1/无盐哈希）
- 使用参数化查询（绝不使用字符串插值 SQL）
- 在使用前验证并清理所有用户输入
- 在认证端点上实现限流
- 设置安全头部（CSP、HSTS、X-Frame-Options）
- 记录安全事件（认证失败、越权尝试）
- 将密钥存储在环境变量或密钥管理器中（绝不存储在源代码中）

### 禁止执行
- 以明文或可逆加密形式存储密码
- 不经验证信任用户输入
- 在日志或错误响应中暴露敏感数据
- 使用弱或已弃用的算法（MD5、SHA-1、DES、ECB 模式）
- 在代码中硬编码密钥或凭证

## 代码示例

### 密码哈希（bcrypt）

```typescript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12; // 最少 10；12 在安全性和性能之间取得平衡

export async function hashPassword(plaintext: string): Promise<string> {
  return bcrypt.hash(plaintext, SALT_ROUNDS);
}

export async function verifyPassword(plaintext: string, hash: string): Promise<boolean> {
  return bcrypt.compare(plaintext, hash);
}
```

### 参数化 SQL 查询（Node.js / pg）

```typescript
// 绝不：`SELECT * FROM users WHERE email = '${email}'`
// 始终：使用位置参数
import { Pool } from 'pg';
const pool = new Pool();

export async function getUserByEmail(email: string) {
  const { rows } = await pool.query(
    'SELECT id, email, role FROM users WHERE email = $1',
    [email]  // 值单独传递 —— 绝不插值
  );
  return rows[0] ?? null;
}
```

### 使用 Zod 进行输入验证

```typescript
import { z } from 'zod';

const LoginSchema = z.object({
  email: z.string().email().max(254),
  password: z.string().min(8).max(128),
});

export function validateLoginInput(raw: unknown) {
  const result = LoginSchema.safeParse(raw);
  if (!result.success) {
    // 返回通用错误 —— 绝不回显原始输入
    throw new Error('Invalid credentials format');
  }
  return result.data;
}
```

### JWT 验证

```typescript
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET!; // 绝不硬编码

export function verifyToken(token: string): jwt.JwtPayload {
  // 如果已过期、被篡改或算法错误则抛出异常
  const payload = jwt.verify(token, JWT_SECRET, {
    algorithms: ['HS256'],   // 显式白名单算法
    issuer: 'your-app',
    audience: 'your-app',
  });
  if (typeof payload === 'string') throw new Error('Invalid token payload');
  return payload;
}
```

### 保护端点安全 —— 完整流程

```typescript
import express from 'express';
import rateLimit from 'express-rate-limit';
import helmet from 'helmet';

const app = express();
app.use(helmet()); // 设置 CSP、HSTS、X-Frame-Options 等
app.use(express.json({ limit: '10kb' })); // 限制 payload 大小

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 分钟
  max: 10,                   // 每个 IP 每个窗口最多 10 次尝试
  standardHeaders: true,
  legacyHeaders: false,
});

app.post('/api/login', authLimiter, async (req, res) => {
  // 1. 验证输入
  const { email, password } = validateLoginInput(req.body);

  // 2. 认证 —— 参数化查询，常量时间比较
  const user = await getUserByEmail(email);
  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    // 通用消息 —— 不透露邮箱是否存在
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // 3. 授权 —— 签发有作用域、短生命周期的 token
  const token = jwt.sign(
    { sub: user.id, role: user.role },
    JWT_SECRET,
    { algorithm: 'HS256', expiresIn: '15m', issuer: 'your-app', audience: 'your-app' }
  );

  // 4. 安全响应 —— token 放在 httpOnly cookie 中，而非响应体
  res.cookie('token', token, { httpOnly: true, secure: true, sameSite: 'strict' });
  return res.json({ message: 'Authenticated' });
});
```

## 输出模板

实现安全功能时，需提供：
1. Safe 的实现代码
2. 注明安全注意事项
3. 配置要求（环境变量、头部）
4. 测试建议

## 知识参考

OWASP Top 10、bcrypt/argon2、JWT、OAuth 2.0、OIDC、CSP、CORS、限流、输入验证、输出编码、加密（AES、RSA）、TLS、安全头部
