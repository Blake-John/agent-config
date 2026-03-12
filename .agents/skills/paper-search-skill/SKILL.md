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

1. 根据领域选择合适的搜索工具：
   - CS/物理：优先使用 arXiv 或 Semantic Scholar
   - 医学/生物：优先使用 PubMed 或 bioRxiv
   - 密码学：使用 IACR ePrint Archive
   - 全面搜索：使用 Google Scholar 或 Semantic Scholar（覆盖所有领域）

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

## 示例交互

### 示例 1：搜索论文
**用户**："我需要找一些关于 transformer 注意力机制的 recent papers"
**响应**：在 arXiv、Semantic Scholar 和 Google Scholar 上搜索 transformer attention，呈现前 10 - 20 个结果及摘要

### 示例 2：使用 Semantic Scholar 搜索
**用户**："帮我用 Semantic Scholar 找一下 GPT-4 相关的论文，要最新的"
**响应**：使用 search_semantic_scholar 搜索 GPT-4，结果包含引用数、影响力等信息

### 示例 3：下载特定论文
**用户**："能下载 'Attention Is All You Need' 这篇论文吗？"
**响应**：搜索相关文献，并使用 arXiv ID 下载 PDF，然后总结关键发现

### 示例 4：阅读和总结
**用户**："这篇论文的主要发现是什么：1706.03762？"
**响应**：下载并阅读论文，总结摘要、研究方法和关键结果

### 示例 5：领域研究
**用户**："我想了解一下最近在计算物理领域的研究历程和最新进展，能帮我找一些相关论文吗？"
**响应**：首先分析 '计算物理' 这个主题，然后列出相关的关键词，使用相应的来源搜索相关论文，分析查找到的论文的重要性以及权威性，找最重要，最前沿的论文，提供清晰的结果和摘要

### 示例 6：入门学习
**用户**： "我想学习如何进行半导体能带的计算，请你帮我查找相应的文献，并为我列出学习的规划"
**响应**：
- 首先分析用户的需求：'学习'，'查找文献'，'学习规划'，以及用户要研究的领域 '计算物理'，'半导体'，'能带计算'
- 分析要搜索的关键词，需要包含用户提供的关键词，也可以自行扩展、补充关键词搜索
- 然后根据用户要研究的领域，使用工具在相应的来源上用分析好的关键词进行搜索，得到搜索结果
- 得到搜索结果后首先呈现搜索结果
- 然后总结这些论文专注于什么，给出一个简要的报告
- 最后根据知识的学习逻辑、难易程度给出一个学习规划

## 错误处理

- 如果找不到论文：尝试其他来源或建议用户提供更具体的信息
- 如果下载失败：解释限制并提供论文详情（DOI、arXiv ID），以便用户直接访问
- 如果论文需要付费：指出这一点，并建议 arXiv 版本或联系作者

## 输出格式

始终提供：
1. 带有论文元数据的清晰搜索结果
2. 下载时：确认文件位置
3. 总结时：结构化的关键发现
4. 下一步：询问用户接下来想做什么
