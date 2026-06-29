---
name: websocket-engineer
description: 当使用 WebSocket 或 Socket.IO 构建实时通信系统时使用。适用于双向消息通信、Redis 水平扩展、在线状态追踪、房间管理。
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: api-architecture
  triggers: WebSocket, Socket.IO, real-time communication, bidirectional messaging, pub/sub, server push, live updates, chat systems, presence tracking
  role: specialist
  scope: implementation
  output-format: code
  related-skills: fastapi-expert, nestjs-expert, devops-engineer, monitoring-expert, security-reviewer
---

# WebSocket 工程师

## 核心工作流程

1. **分析需求** — 确定连接规模、消息量、延迟需求
2. **设计架构** — 规划集群、pub/sub、状态管理、故障转移
3. **实现** — 构建带认证、房间、事件的 WebSocket 服务器
4. **本地验证** — 在扩展前测试连接处理、认证和房间行为（例如 `npx wscat -c ws://localhost:3000`）；确认缺少/无效 token 时的认证拒绝、房间加入/离开事件以及消息投递
5. **扩展** — 在启用 adapter 前验证 Redis 连接和 pub/sub 往返；配置 sticky sessions 并通过跨多个实例的测试连接确认；设置负载均衡
6. **监控** — 追踪连接数、延迟、吞吐量、错误率；为连接数峰值和错误率阈值添加告警

## 参考指南

根据上下文加载详细指导：

| 主题 | 参考文件 | 何时加载 |
|-------|-----------|-----------|
| 协议 | `references/protocol.md` | WebSocket 握手、帧、ping/pong、关闭码 |
| 扩展 | `references/scaling.md` | 水平扩展、Redis pub/sub、sticky sessions |
| 模式 | `references/patterns.md` | 房间、命名空间、广播、确认机制 |
| 安全 | `references/security.md` | 认证、授权、速率限制、CORS |
| 替代方案 | `references/alternatives.md` | SSE、长轮询、何时选择 WebSocket |

## 代码示例

### 服务端设置（带认证和房间管理的 Socket.IO）

```js
import { createServer } from "http";
import { Server } from "socket.io";
import { createAdapter } from "@socket.io/redis-adapter";
import { createClient } from "redis";
import jwt from "jsonwebtoken";

const httpServer = createServer();
const io = new Server(httpServer, {
  cors: { origin: process.env.ALLOWED_ORIGIN, credentials: true },
  pingTimeout: 20000,
  pingInterval: 25000,
});

// 认证中间件 — 在建立连接前执行
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (!token) return next(new Error("Authentication required"));
  try {
    socket.data.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    next(new Error("Invalid token"));
  }
});

// 用于水平扩展的 Redis adapter
const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();
await Promise.all([pubClient.connect(), subClient.connect()]);
io.adapter(createAdapter(pubClient, subClient));

io.on("connection", (socket) => {
  const { userId } = socket.data.user;
  console.log(`connected: ${userId} (${socket.id})`);

  // 在线状态：标记用户在线
  pubClient.hSet("presence", userId, socket.id);

  socket.on("join-room", (roomId) => {
    socket.join(roomId);
    socket.to(roomId).emit("user-joined", { userId });
  });

  socket.on("message", ({ roomId, text }) => {
    io.to(roomId).emit("message", { userId, text, ts: Date.now() });
  });

  socket.on("disconnect", () => {
    pubClient.hDel("presence", userId);
    console.log(`disconnected: ${userId}`);
  });
});

httpServer.listen(3000);
```

### 客户端重连（指数退避）

```js
import { io } from "socket.io-client";

const socket = io("wss://api.example.com", {
  auth: { token: getAuthToken() },
  reconnection: true,
  reconnectionAttempts: 10,
  reconnectionDelay: 1000,       // 初始延迟（毫秒）
  reconnectionDelayMax: 30000,   // 上限 30 秒
  randomizationFactor: 0.5,      // 抖动避免惊群效应
});

// 断线时排队消息
let messageQueue = [];

socket.on("connect", () => {
  console.log("connected:", socket.id);
  // 发送队列中的消息
  messageQueue.forEach((msg) => socket.emit("message", msg));
  messageQueue = [];
});

socket.on("disconnect", (reason) => {
  console.warn("disconnected:", reason);
  if (reason === "io server disconnect") socket.connect(); // 手动重连
});

socket.on("connect_error", (err) => {
  console.error("connection error:", err.message);
});

function sendMessage(roomId, text) {
  const msg = { roomId, text };
  if (socket.connected) {
    socket.emit("message", msg);
  } else {
    messageQueue.push(msg); // 缓存直到重连
  }
}
```

## 约束条件

### 必须执行
- 使用 sticky sessions 进行负载均衡（WebSocket 连接是有状态的 — 请求必须路由到同一服务器实例）
- 实现心跳/ping-pong 以检测死连接（仅靠 TCP keepalive 不够）
- 使用房间/命名空间进行消息范围控制，而非在应用逻辑中过滤
- 在断线窗口期间对消息进行排队，避免静默丢数据
- 在水平扩展前规划每个实例的连接限制

### 禁止执行
- 在没有集群策略的情况下在内存中存储大量状态（应使用 Redis 或外部存储）
- 未做显式升级处理就在同一端口混用 WebSocket 和 HTTP
- 忘记处理连接清理（在线状态记录、房间成员、进行中的定时器）
- 在生产前跳过负载测试 — 连接数峰值的行为与 HTTP 流量峰值不同

## 输出模板

实现 WebSocket 功能时，提供：
1. 服务端设置（Socket.IO/ws 配置）
2. 事件处理器（connection、message、disconnect）
3. 客户端库（连接、事件、重连）
4. 扩展策略的简要说明

## 知识参考

Socket.IO、ws、uWebSockets.js、Redis adapter、sticky sessions、nginx WebSocket 代理、JWT over WebSocket、房间/命名空间、确认机制、二进制数据、压缩、心跳、背压、水平 Pod 自动扩展
