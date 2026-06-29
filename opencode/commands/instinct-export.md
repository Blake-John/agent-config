---
description: 导出 instinct 以供分享
agent: build
---

# Instinct 导出命令

从 continuous-learning-v2 系统导出 instinct：$ARGUMENTS

## 导出选项

### 导出全部
```
/instinct-export
```

### 仅导出高置信度
```
/instinct-export --min-confidence 0.8
```

### 按类别导出
```
/instinct-export --category coding
```

### 导出到指定路径
```
/instinct-export --output ./my-instincts.json
```

## 导出格式

```json
{
  "instincts": [
    {
      "id": "instinct-123",
      "trigger": "[场景描述]",
      "action": "[建议操作]",
      "confidence": 0.85,
      "category": "coding",
      "applications": 10,
      "successes": 9,
      "source": "session-observation"
    }
  ],
  "metadata": {
    "version": "1.0",
    "exported": "2025-01-15T10:00:00Z",
    "author": "username",
    "total": 25
  }
}
```

## 导出报告

```
导出摘要
=========
输出：./instincts-export.json
总计：X
过滤后：Y
已导出：Z

类别：
- coding: N
- testing: N
- security: N

按置信度排序：
1. [trigger] (0.XX)
2. [trigger] (0.XX)
```

---

**提示**：导出高置信度 instinct（>0.8）以获得更好的分享质量。
