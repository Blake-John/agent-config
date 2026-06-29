# Harness 审计命令

运行确定性的仓库 harness 审计并返回优先级评分卡。

## 用法

`/harness-audit [scope] [--format text|json] [--root path]`

- `scope`（可选）：`repo`（默认）、`hooks`、`skills`、`commands`、`agents`
- `--format`：输出格式（`text` 默认，`json` 用于自动化）
- `--root`：审计指定路径而非当前工作目录

## 确定性引擎

始终运行：

```bash
node scripts/harness-audit.js <scope> --format <text|json> [--root <path>]
```

此脚本是评分和检查的唯一信源。不要自行添加额外维度。

评分标准版本：`2026-03-30`

脚本计算 7 个固定类别（各 0-10 归一化）：

1. 工具覆盖
2. 上下文效率
3. 质量门禁
4. 记忆持久性
5. 评估覆盖
6. 安全护栏
7. 成本效率

## 输出约定

返回：

1. `overall_score` / `max_score`（repo 为 70，范围审计更少）
2. 各类别得分和具体发现
3. 失败的检查及精确文件路径
4. 确定性输出的前 3 项行动（`top_actions`）
5. 建议下一步应用的 ECC skill

## 示例结果

```text
Harness Audit (repo): 66/70
- Tool Coverage: 10/10
- Context Efficiency: 9/10
- Quality Gates: 10/10

Top 3 Actions:
1) [Security Guardrails] 添加安全检查 (hooks/hooks.json)
2) [Tool Coverage] 同步命令文件 (.opencode/commands/harness-audit.md)
3) [Eval Coverage] 增加自动化测试覆盖 (tests/)
```
