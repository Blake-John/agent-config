---
name: paper-search-skill
description: 学术论文研究助手。帮助用户搜索、下载、阅读和管理学术论文。当用户提到搜索论文、查找学术文献、寻找研究资料、下载论文、阅读论文、查找某个研究主题的最新进展时，必须使用此 skill。此 skill 提供完整的学术论文研究工作流，包括搜索、筛选、下载和阅读论文核心内容。
---

# Paper Search Skill

学术论文研究助手，帮助用户搜索、下载和管理学术论文。

## 可用工具

此 skill 使用 Paper Search MCP，提供以下工具：

- **search_arxiv** - 搜索 arXiv 预印本（物理、数学、计算机等）
- **search_pubmed** - 搜索 PubMed（医学和生物文献）
- **search_biorxiv** - 搜索 bioRxiv（生物学预印本）
- **search_medrxiv** - 搜索 medRxiv（医学预印本）
- **search_google_scholar** - 搜索 Google 学术
- **search_semantic_scholar** - 搜索 Semantic Scholar（综合学术搜索引擎）
- **search_iacr** - 搜索 IACR ePrint Archive（密码学相关论文）
- **download_arxiv** / **read_arxiv_paper** - 下载或读取 arXiv PDF
- **download_pubmed** / **read_pubmed_paper** - 访问 PubMed 论文
- **download_biorxiv** / **read_biorxiv_paper** - 下载或读取 bioRxiv PDF
- **download_medrxiv** / **read_medrxiv_paper** - 下载或读取 medRxiv PDF

## 触发场景

当用户有以下需求时，必须使用此 skill：

- 搜索学术论文
- 查找某个研究主题的最新论文
- 下载论文 PDF
- 阅读并理解论文内容
- 查找特定作者的研究
- 比较不同来源的研究
- 获取论文的摘要和关键信息

## 工作流程

### 步骤 1：理解研究需求

当用户请求论文研究时：

1. 明确研究主题或问题
2. 根据领域选择合适的来源：
   - **计算机科学、物理、数学**：arXiv, Semantic Scholar
   - **密码学**：IACR ePrint Archive
   - **医学、生物学**：PubMed、bioRxiv、medRxiv
   - **通用研究**：Google Scholar、Semantic Scholar（覆盖所有领域）
   - **综合搜索**：Semantic Scholar（强大的论文检索和引用分析）
3. 询问具体要求：
   - 时间范围（近期论文 vs 经典论文），默认最经典的论文（开山之作、高引用论文）
   - 需要的论文数量，默认 10 - 20 篇
   - 特定作者或期刊，默认不限制

### 步骤 2：搜索论文

1. **根据需求选择搜索策略**:
   - 经典论文 → 策略1 + Google Scholar + arXiv
   - 最新进展 → 策略2 + Google Scholar + arXiv
   - 了解领域 → 策略3（综述）
   - 方法细节 → 策略4
   - 实际应用 → 策略7

2. **执行搜索**: 根据领域选择合适的搜索工具：
   - CS/物理：优先使用 arXiv 或 Semantic Scholar
   - 医学/生物：优先使用 PubMed 或 bioRxiv
   - 密码学：使用 IACR ePrint Archive
   - 全面搜索：使用 Google Scholar 或 Semantic Scholar（覆盖所有领域）

> 注意：如果无法连接到某个数据源，请使用 arXiv 作为备选数据源进行搜索。

2. 提供结果包含：
   - 论文标题
   - 作者
   - 发表日期
   - 来源
   - 摘要（如果有）
   - arXiv ID / DOI / PMID / Semantic Scholar Paper ID
   - 引用次数（如果有）
   - 关键词（如果有）
   - 直接下载链接（如果可用）

### 步骤 3：呈现结果

清晰格式化结果：

```
## 搜索结果：[主题]

### 论文 1：[标题]
- **作者**：[作者列表]
- **日期**：[发表日期]
- **来源**：[arXiv/PubMed/bioRxiv 等]
- **ID**：[arXiv ID / DOI / PMID]
- **摘要**：[简要总结]
- **关键词**：[关键词列表]
- **引用次数**：[引用次数]
- **要点**：[3-5个要点]
- **PDF**：[直接下载链接]
- **原始链接**：[原始论文链接]

### 论文 2：...
...
### 论文 N：...
```

### 步骤 4：下载和阅读（按需）

当用户想要阅读特定论文时：

1. 首先尝试使用合适的工具下载 PDF：
   - 使用 `download_arxiv` 下载 arXiv 论文（使用 arXiv ID）
   - 使用 `download_pubmed` 下载 PubMed 论文（使用 PMID）
   - 使用 `download_biorxiv` 下载 bioRxiv 论文（使用 DOI）
   - 使用 `download_medrxiv` 下载 medRxiv 论文（使用 DOI）

2. 如果 PDF 下载不可用，尝试读取论文内容：
   - `read_arxiv_paper` - 从 arXiv PDF 提取文本
   - `read_biorxiv_paper` - 从 bioRxiv PDF 提取文本
   - `read_medrxiv_paper` - 从 medRxiv PDF 提取文本

3. 总结论文的关键发现：
   - 主要贡献
   - 研究方法
   - 关键结果
   - 结论

### 步骤 5：组织和跟进

提供结果后：

- 询问用户是否想要下载特定论文
- 如果需要可以搜索更多论文
- 可以深入分析特定论文
- 如果有多篇相关论文，可以创建对比总结

## 搜索策略

### 策略 1：经典论文搜索（奠基性工作）

**目标**: 找到领域的开创性论文、高被引论文

**搜索策略**:

1. 使用 `search_google_scholar` 以及 `search_arxiv` 搜索核心关键词
2. 按引用数排序，优先选择被引 > 100 的论文
3. 搜索 "foundational", "seminal", "pioneering" + 领域关键词
4. 查找领域经典论文的直接引用

**关键词策略**:

- `[领域] foundation`
- `[领域] seminal work`
- `[领域] classic paper`
- `[核心概念] original`

**时间策略**: 优先 5-15 年前的论文

---

### 策略 2：最新进展搜索（前沿研究）

**目标**: 找到近 1-2 年的最新研究

**搜索策略**:

1. 使用 `search_arxiv` 搜索（最新预印本）
2. 使用 `search_google_scholar` 并设置时间筛选
3. 搜索顶会论文（NeurIPS, ICML, ICLR, CVPR, ACL 等）

**关键词策略**:

- `[领域] 2024`
- `[领域] 2025`
- `[领域] recent advances`
- `[领域] state of the art`
- `[核心概念] recent`

**时间策略**: 优先最近 2 年的论文

---

### 策略 3：综述论文搜索

**目标**: 找到领域的全面综述

**搜索策略**:

1. 使用 `search_google_scholar` 或 `search_semantic_scholar` 或 `search_arxiv` 搜索
2. 搜索 "survey", "review", "tutorial", "overview" + 领域关键词
3. 优先选择发表在权威期刊的综述

**关键词策略**:

- `[领域] survey`
- `[领域] review`
- `[领域] comprehensive review`
- `[领域] tutorial`
- `[领域] state of the art survey`

**筛选标准**:

- 发表时间：近 5 年
- 引用数：越高越好
- 来源：权威期刊/会议

---

### 策略 4：方法论论文搜索

**目标**: 找到具体方法的技术细节

**搜索策略**:

1. 明确方法名称或变体
2. 使用多个同义词搜索
3. 查找原始论文（原始提出者）

**关键词策略**:

- `[方法名] paper`
- `[方法名] original paper`
- `[方法名] proposed`
- `[方法名] implementation`

---

### 策略 5：对比学习搜索

**目标**: 找到方法对比、基准测试论文

**搜索策略**:

1. 搜索 "comparison", "benchmark", "evaluation" + 领域
2. 查找包含 ablation study 的论文
3. 搜索方法的消融实验论文

**关键词策略**:

- `[领域] benchmark`
- `[领域] comparison`
- `[领域] evaluation`
- `[方法] vs`
- `[方法] ablation study`

---

### 策略 6：跨领域应用搜索

**目标**: 找到方法在不同领域的应用

**搜索策略**:

1. 搜索 "application" + 领域
2. 搜索 "[方法] + [目标领域]"
3. 查找领域特定的论文

**关键词策略**:

- `[方法] medical`
- `[方法] healthcare`
- `[方法] finance`
- `[方法] [新领域]`

---

### 策略 7：代码实现搜索

**目标**: 找到有开源代码的论文

**搜索策略**:

1. 在 Google Scholar / arXiv 中筛选 "GitHub" 或 "Code" 链接
2. 搜索 "official implementation"
3. 查找 Papers with Code 网站

**关键词策略**:

- `[论文标题] github`
- `[方法] official code`
- `[方法] implementation`

---

## 搜索策略选择流程

```
用户需求分析
      │
      ▼
┌─────────────────┐
│ 是什么类型的需求？ │
└─────────────────┘
      │
      ├─▶ 了解领域概览 ──▶ 策略3（综述）+ 策略1（经典）
      │
      ├─▶ 学习特定方法 ──▶ 策略4（方法论）+ 策略1（奠基）
      │
      ├─▶ 了解最新进展 ──▶ 策略2（最新）+ 策略5（对比）
      │
      ├─▶ 应用到新领域 ──▶ 策略6（跨领域）
      │
      └─▶ 实际项目应用 ──▶ 策略7（代码）+ 策略5（基准）

选择合适的数据源组合执行搜索
```

---

## 关键词扩展技巧

### 1. 同义词扩展

- "neural network" → "neural net", "deep learning", "DL"
- "machine learning" → "ML", "statistical learning"
- "natural language processing" → "NLP", "text mining"

### 2. 上位词/下位词

- 上位词：更广泛的类别
- 下位词：更具体的子领域

### 3. 方法变体名称

- 原始名称 + "v2", "new", "improved"
- 会议/期刊名称 + 方法名

### 4. 作者名

- 领域知名研究者
- 最近高产的团队

### 5. 会议/期刊

- CVPR, NeurIPS, ICML, ICLR, ACL, EMNLP, AAAI, IJCAI
- Nature, Science, Cell, Lancet, NEJM

---

## 多轮搜索策略

### 第一轮：广度搜索

- 使用通用关键词
- 多个数据库同时搜索
- 收集 20+ 候选论文

### 第二轮：精炼搜索

- 基于第一轮结果，调整关键词
- 聚焦于高相关度论文
- 查找综述论文

### 第三轮：深度搜索

- 查找特定论文的引用
- 查找作者的其他相关工作
- 查找后续改进工作

---

## 结果筛选标准

### 必须考虑的维度

| 维度 | 说明 | 权重 |
|------|------|------|
| 相关度 | 与研究问题的匹配程度 | 高 |
| 引用数 | 论文影响力指标 | 中 |
| 时间 | 论文时效性 | 中 |
| 来源 | 期刊/会议权威性 | 中 |
| 可获取性 | 是否有 PDF | 高 |

### 优先级排序

1. **P0 - 必读**: 综述 + 高相关 + 高引用
2. **P1 - 重要**: 方法论 + 高相关 + 中等引用
3. **P2 - 参考**: 最新 + 中等相关

---

## 获得更好结果的技巧

1. **使用具体关键词** - 更具体的搜索词会得到更好的结果
2. **尝试多个来源** - 不同数据库覆盖范围不同：
   - **Semantic Scholar**：适合综合搜索，有引用关系分析
   - **Google Scholar**：适合全面搜索
   - **arXiv**：适合 CS/物理最新预印本
3. **优先查看近期论文** - 对于当前研究主题，近期论文通常更相关
4. **使用作者姓名** - 如果在寻找特定研究人员的工作
5. **组合搜索** - 先广泛搜索，然后根据结果细化
6. **利用 Semantic Scholar 的引用图** - 可以追踪论文的影响力和相关研究

> 注意：当其中一个来源无法得到结果的时候，需要使用另一来源进行补充搜索。

## 示例交互

### 示例 1：了解领域概览

**用户**："我想了解一下大语言模型（LLM）领域的最新进展"
**策略选择**：策略3（综述）+ 策略2（最新）
**执行**：搜索 "LLM survey review" 和 "LLM 2024 2025"

### 示例 2：学习具体方法

**用户**："我想深入了解 Transformer 架构的原理"
**策略选择**：策略4（方法论）+ 策略1（奠基）
**执行**：搜索 "Transformer original paper" 和 "Attention is All You Need"

### 示例 3：实际项目应用

**用户**："我想用 BERT 做文本分类，有推荐的论文和代码吗？"
**策略选择**：策略7（代码）+ 策略5（基准）
**执行**：搜索 "BERT text classification github" 和 "BERT benchmark"

### 示例 4：跨领域应用

**用户**："我想把深度学习应用到医学影像诊断"
**策略选择**：策略6（跨领域）
**执行**：搜索 "deep learning medical imaging" 和 "CNN medical diagnosis"

### 示例 5：了解最新前沿

**用户**："帮我看看最近的 AI 有什么新突破？"
**策略选择**：策略2（最新）+ 策略5（对比）
**执行**：在 arXiv 搜索最近 6 个月的论文，关注 NeurIPS/ICML 最新论文

### 示例 6：深度研究

**用户**："我要写一篇关于强化学习的综述论文"
**策略选择**：多轮搜索（综述→经典→最新）
**执行**：

1. 先找强化学习 survey
2. 按时间线梳理发展脉络
3. 识别主要流派和方法
4. 收集最新的未发表工作

## 错误处理

- 如果找不到论文：尝试其他来源或建议用户提供更具体的信息
- 如果下载失败：解释限制并提供论文详情（DOI、arXiv ID），以便用户直接访问
- 如果论文需要付费：指出这一点，并建议 arXiv 版本或联系作者

## 数据源选择指南

### 按领域选择

| 领域 | 首选数据源 | 备用数据源 | 特点 |
|------|-----------|-----------|------|
| 计算机科学 | arXiv, Semantic Scholar | Google Scholar | 预印本多，更新快 |
| 机器学习 | arXiv, Semantic Scholar | Google Scholar | 快速获取最新进展 |
| 人工智能 | arXiv, Semantic Scholar | Google Scholar | 跨领域综合 |
| 密码学 | IACR ePrint | Google Scholar | 专业数据库 |
| 医学 | PubMed, bioRxiv | Google Scholar | 同行评审为主 |
| 生物学 | PubMed, bioRxiv, bioRxiv | Google Scholar | 研究预印本 |
| 物理学 | arXiv | Google Scholar | 覆盖全面 |
| 数学 | arXiv | Google Scholar | 预印本为主 |
| 工程 | Google Scholar, Semantic Scholar | - | 综合搜索 |
| 化学 | PubMed, Google Scholar | - | 跨学科 |
| 其他 | Google Scholar | Semantic Scholar | 覆盖最广 |

### 按需求选择

| 需求 | 推荐数据源 | 原因 |
|------|-----------|------|
| 最新预印本 | arXiv | 更新最快 |
| 高引论文 | Semantic Scholar | 引用分析强 |
| 全面覆盖 | Google Scholar | 数据库最大 |
| 特定领域 | 专用数据库 | 质量更高 |
| 引用关系 | Semantic Scholar | 引用图完整 |
| 同行评审 | PubMed | 医学权威 |

---

## 输出格式

始终提供：

1. 带有论文元数据的清晰搜索结果
2. 下载时：确认文件位置
3. 总结时：结构化的关键发现
4. 下一步：询问用户接下来想做什么
