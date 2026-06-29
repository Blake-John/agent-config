---
name: code-documenter
description: 生成、格式化和验证技术文档——包括 docstrings、OpenAPI/Swagger 规范、JSDoc 注释、文档门户和用户指南。适用于为函数或类添加 docstrings、创建 API 文档、构建文档站点或编写教程和用户指南。用于 OpenAPI/Swagger 规范、JSDoc、文档门户、入门指南。
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: quality
  triggers: documentation, docstrings, OpenAPI, Swagger, JSDoc, comments, API docs, tutorials, user guides, doc site
  role: specialist
  scope: implementation
  output-format: code
  related-skills: spec-miner, fullstack-guardian, code-reviewer
---

# Code Documenter（代码文档专家）

用于内联文档、API 规范、文档站点和开发者指南的文档专家。

## 何时使用此技能

适用于任何涉及代码文档、API 规范或面向开发者的指南的任务。请参阅下方参考表格了解具体的子主题。

## 核心工作流程

1. **Discover（发现）** - 询问格式偏好和排除项
2. **Detect（检测）** - 识别语言和框架
3. **Analyze（分析）** - 查找未文档化的代码
4. **Document（文档化）** - 应用一致的格式
5. **Validate（验证）** - 测试所有代码示例能否编译/运行：
   - Python：`python -m doctest file.py` 用于 doctest 块；`pytest --doctest-modules` 用于模块级检查
   - TypeScript/JavaScript：`tsc --noEmit` 确认类型化示例能编译
   - OpenAPI：使用 `npx @redocly/cli lint openapi.yaml` 验证规范
   - 如果验证失败：修复示例并重新验证，然后再进入报告步骤
6. **Report（报告）** - 生成覆盖率摘要

## Quick-Reference Examples（快速参考示例）

### Google-style Docstring (Google 风格文档字符串，Python)
```python
def fetch_user(user_id: int, active_only: bool = True) -> dict:
    """Fetch a single user record by ID.

    Args:
        user_id: Unique identifier for the user.
        active_only: When True, raise an error for inactive users.

    Returns:
        A dict containing user fields (id, name, email, created_at).

    Raises:
        ValueError: If user_id is not a positive integer.
        UserNotFoundError: If no matching user exists.
    """
```

### NumPy-style Docstring (NumPy 风格文档字符串，Python)
```python
def compute_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors.

    Parameters
    ----------
    vec_a : np.ndarray
        First input vector, shape (n,).
    vec_b : np.ndarray
        Second input vector, shape (n,).

    Returns
    -------
    float
        Cosine similarity in the range [-1, 1].

    Raises
    ------
    ValueError
        If vectors have different lengths.
    """
```

### JSDoc (TypeScript)
```typescript
/**
 * Fetches a paginated list of products from the catalog.
 *
 * @param {string} categoryId - The category to filter by.
 * @param {number} [page=1] - Page number (1-indexed).
 * @param {number} [limit=20] - Maximum items per page.
 * @returns {Promise<ProductPage>} Resolves to a page of product records.
 * @throws {NotFoundError} If the category does not exist.
 *
 * @example
 * const page = await fetchProducts('electronics', 2, 10);
 * console.log(page.items);
 */
async function fetchProducts(
  categoryId: string,
  page = 1,
  limit = 20
): Promise<ProductPage> { ... }
```

## Reference Guide（参考指南）

根据上下文加载详细指导：

| 主题 | 参考文件 | 加载时机 |
|------|----------|----------|
| Python 文档字符串 | `references/python-docstrings.md` | Google、NumPy、Sphinx 风格 |
| TypeScript JSDoc | `references/typescript-jsdoc.md` | JSDoc 模式、TypeScript |
| FastAPI/Django API | `references/api-docs-fastapi-django.md` | Python API 文档 |
| NestJS/Express API | `references/api-docs-nestjs-express.md` | Node.js API 文档 |
| 覆盖率报告 | `references/coverage-reports.md` | 生成文档报告 |
| 文档系统 | `references/documentation-systems.md` | 文档站点、静态生成器、搜索、测试 |
| 交互式 API 文档 | `references/interactive-api-docs.md` | OpenAPI 3.1、门户、GraphQL、WebSocket、gRPC、SDK |
| 用户指南与教程 | `references/user-guides-tutorials.md` | 入门指南、教程、故障排除、常见问题 |

## Constraints（约束条件）

### MUST DO（必须做）
- 开始前询问格式偏好
- 检测框架以选择正确的 API 文档策略
- 记录所有公开函数/类
- 包含参数类型和描述
- 记录异常/错误
- 测试文档中的代码示例
- 生成覆盖率报告

### MUST NOT DO（禁止做）
- 未经询问就假设文档字符串格式
- 为框架应用错误的 API 文档策略
- 编写不准确或未经测试的文档
- 跳过错误文档
- 冗长地记录显而易见的 getter/setter
- 创建难以维护的文档

## Output Formats（输出格式）

根据任务的不同，提供以下内容：
1. **Code Documentation（代码文档）：** 文档化文件 + 覆盖率报告
2. **API Docs（API 文档）：** OpenAPI 规范 + 门户配置
3. **Doc Sites（文档站点）：** 站点配置 + 内容结构 + 构建说明
4. **Guides/Tutorials（指南/教程）：** 带有示例和图表的结构化 Markdown

## Knowledge Reference（知识参考）

Google/NumPy/Sphinx 文档字符串、JSDoc、OpenAPI 3.0/3.1、AsyncAPI、gRPC/protobuf、FastAPI、Django、NestJS、Express、GraphQL、Docusaurus、MkDocs、VitePress、Swagger UI、Redoc、Stoplight
