---
description: 从外部源导入 instinct
agent: build
---

# Instinct 导入命令

从文件或 URL 导入 instinct：$ARGUMENTS

## 导入源

### 文件导入
```
/instinct-import path/to/instincts.json
```

### URL 导入
```
/instinct-import https://example.com/instincts.json
```

### 团队分享导入
```
/instinct-import @teammate/instincts
```

## 导入流程

1. **验证格式** — 检查 JSON 结构
2. **去重** — 跳过已存在的 instinct
3. **调整置信度** — 导入的 instinct 置信度降低（×0.8）
4. **合并** — 添加到本地 instinct 存储
5. **报告** — 显示导入摘要

## 冲突解决

- 保留置信度较高的版本
- 合并应用次数
- 更新时间戳

---

**提示**：导入后用 `/instinct-status` 检查导入结果。
