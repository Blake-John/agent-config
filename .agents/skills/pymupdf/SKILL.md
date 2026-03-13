---
name: pymupdf
description: >
  使用 PyMuPDF4LLM 处理 PDF 文献的完整工具集。当用户提到提取 PDF 文本、转换 PDF 为 Markdown、从 PDF 提取表格、将 PDF 转换为 JSON、处理扫描版 PDF (OCR)、批量处理多个 PDF、或需要将 PDF 文档准备用于 RAG/LLM 应用时，必须使用此 skill。此 skill 提供 PDF 文本提取、格式化输出、图像提取、元数据获取、表格处理等完整工作流。
compatibility:
  tools:
    - bash
    - write
    - read
    - glob
  dependencies:
    - pymupdf4llm
    - pymupdf
    - pymupdf-layout
    - opencv-python
---

# PyMuPDF Skill

使用 PyMuPDF4LLM 处理 PDF 文献的完整指南。

## 概述

PyMuPDF4LLM 是 PyMuPDF 的轻量级扩展，专门为 LLM 和 RAG 环境设计。它可以将 PDF 转换为干净的、结构化的 Markdown、JSON 或纯文本格式，支持：

- Markdown/JSON/TXT 输出格式
- 多列页面支持
- 布局分析以更好地理解文档结构
- 页块输出 (page chunking)
- LlamaIndex 和 LangChain 集成
- OCR 光学字符识别支持

## 安装

```bash
pip install pymupdf4llm
```

安装包含布局分析和自动 OCR 的完整支持：

```bash
pip install pymupdf4llm pymupdf-layout opencv-python
```

## 核心 API

### 1. 转换为 Markdown (主要用途)

```python
import pymupdf4llm

# 基本转换 - 转换为 Markdown
md_text = pymupdf4llm.to_markdown("input.pdf")

# 激活布局模式 (推荐)
import pymupdf.layout
import pymupdf4llm

md_text = pymupdf4llm.to_markdown("input.pdf")
```

**关键参数：**

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `pages` | list/range/None | None | 要处理的页面，如 `[0, 1, 2]` 或 `range(1, 5)` |
| `page_chunks` | bool | False | True 时返回字典列表，每页一个 |
| `header` | bool | True | 是否包含页眉 |
| `footer` | bool | True | 是否包含页脚 |
| `write_images` | bool | False | 将图像保存到文件 |
| `embed_images` | bool | False | 将图像嵌入为 base64 |
| `use_ocr` | bool | True | 自动对图像页面进行 OCR |
| `extract_words` | bool | False | 提取单词级别的位置信息 |
| `table_strategy` | str | 'lines_strict' | 表格提取策略 |

### 2. 转换为 JSON

```python
import pymupdf.layout
import pymupdf4llm

# 输出包含边界框信息的 JSON
json_text = pymupdf4llm.to_json("input.pdf")
```

JSON 输出包含每个元素的边界框坐标和布局数据。

### 3. 转换为纯文本

```python
import pymupdf.layout
import pymupdf4llm

# 纯文本输出
txt = pymupdf4llm.to_text("input.pdf")
```

### 4. LlamaIndex 集成

```python
import pymupdf4llm

# 获取 LlamaIndex Document 对象
llama_reader = pymupdf4llm.LlamaMarkdownReader()
documents = llama_reader.load_data("input.pdf")
```

### 5. LangChain 集成

```python
from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader("input.pdf")
data = loader.load()
```

## 常用任务

### 任务 1：提取 PDF 文本为 Markdown

```python
import pymupdf4llm
import pathlib

md_text = pymupdf4llm.to_markdown("input.pdf")
pathlib.Path("output.md").write_bytes(md_text.encode())
```

### 任务 2：按页提取文本

```python
import pymupdf4llm

# 提取指定页面 (0-indexed)
pages = [0, 2, 4]  # 第1、3、5页
md_text = pymupdf4llm.to_markdown("input.pdf", pages=pages)

# 或使用 range
md_text = pymupdf4llm.to_markdown("input.pdf", pages=range(0, 3))
```

### 任务 3：提取页面块 (每页一个字典)

```python
import pymupdf4llm

# 返回字典列表，每页一个
page_data = pymupdf4llm.to_markdown("input.pdf", page_chunks=True)

for i, chunk in enumerate(page_data):
    print(f"Page {i+1}:")
    print(chunk["text"][:200])  # 该页的前200个字符
    # 字典包含: text, page_number, bbox 等
```

### 任务 4：去除页眉页脚

```python
import pymupdf.layout
import pymupdf4llm

# 去除页眉和页脚
md_text = pymupdf4llm.to_markdown("input.pdf", header=False, footer=False)
```

### 任务 5：提取图像

```python
import pymupdf4llm

# 图像保存到文件 (./images/ 目录)
md_text = pymupdf4llm.to_markdown("input.pdf", write_images=True)

# 或嵌入为 base64
md_text = pymupdf4llm.to_markdown("input.pdf", embed_images=True)
```

### 任务 6：处理扫描版 PDF (OCR)

```python
import pymupdf4llm

# 默认会自动对图像页面进行 OCR
md_text = pymupdf4llm.to_markdown("input.pdf")

# 或强制使用 OCR
md_text = pymupdf4llm.to_markdown("input.pdf", force_ocr=True)
```

### 任务 7：处理复杂 PDF (忽略图形)

对于包含大量矢量图形导致提取失败的 PDF：

```python
import pymupdf
import pymupdf4llm

doc = pymupdf.open("input.pdf")
hdr_info = pymupdf4llm.IdentifyHeaders(doc)

md_text = ""
for page in doc:
    md_text += pymupdf4llm.to_markdown(
        doc,
        pages=[page.number],
        hdr_info=hdr_info,
        ignore_images=True,
        ignore_graphics=True,
    )
```

### 任务 8：使用 PyMuPDF Document 对象

```python
import pymupdf
import pymupdf4llm

doc = pymupdf.open("input.pdf")
md_text = pymupdf4llm.to_markdown(doc, pages=range(0, min(10, len(doc))))
```

### 任务 9：批量处理多个 PDF

```python
import pymupdf4llm
from pathlib import Path

pdf_files = Path(".").glob("*.pdf")

for pdf in pdf_files:
    md_text = pymupdf4llm.to_markdown(pdf)
    output_file = pdf.with_suffix(".md")
    output_file.write_bytes(md_text.encode())
    print(f"Converted: {pdf.name} -> {output_file.name}")
```

### 任务 10：获取 PDF 元数据

```python
import pymupdf

doc = pymupdf.open("input.pdf")
meta = doc.metadata

print(f"Title: {meta.get('title')}")
print(f"Author: {meta.get('author')}")
print(f"Subject: {meta.get('subject')}")
print(f"Creator: {meta.get('creator')}")
print(f"Producer: {meta.get('producer')}")
print(f"Pages: {len(doc)}")
```

## 工作流程

### 场景 1：深度研究中的文献精读

1. **下载 PDF**: 使用 `paper-search-skill` 下载论文 PDF
2. **转换为 Markdown**: 使用此 skill 转换为 Markdown
3. **提取关键信息**: 使用 `grep` 或 `read` 工具搜索关键内容
4. **生成笔记**: 提取标题、摘要、方法、结论等

```python
import pymupdf.layout
import pymupdf4llm
from pathlib import Path

def extract_paper_summary(pdf_path):
    """提取论文关键信息"""
    # 转换为 Markdown
    md = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)
    
    # 提取第一页作为摘要
    first_page = md[0]["text"] if md else ""
    
    # 提取所有文本
    all_text = "\n\n".join([chunk["text"] for chunk in md])
    
    return {
        "pages": len(md),
        "first_page": first_page[:1000],
        "full_text": all_text
    }

# 使用
result = extract_paper_summary("research_papers/attention_is_all_you_need.pdf")
```

### 场景 2：RAG 文档预处理

```python
import pymupdf.layout
import pymupdf4llm
from langchain.text_splitter import MarkdownTextSplitter

# 转换为 Markdown
md_text = pymupdf4llm.to_markdown("document.pdf")

# 使用 MarkdownTextSplitter 分块
splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.create_documents([md_text])

# 每个 chunk 现在可以用于 embedding
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: {chunk.page_content[:100]}...")
```

### 场景 3：提取表格

```python
import pymupdf.layout
import pymupdf4llm
import json

# 转换为 JSON 格式以获取表格位置信息
json_data = pymupdf4llm.to_json("input.pdf", table_strategy='lines_strict')
data = json.loads(json_data)

# 遍历页面查找表格
for page_data in data:
    if "tables" in page_data:
        for table in page_data["tables"]:
            print(table["content"])
```

## 错误处理

### 问题 1：PDF 包含大量矢量图形导致提取不完整

**症状**: 只提取了部分页面，或某些页面文本丢失

**解决方案**: 使用 `ignore_graphics=True`

```python
md_text = pymupdf4llm.to_markdown("input.pdf", ignore_graphics=True)
```

### 问题 2：OCR 不工作

**症状**: 扫描版 PDF 没有提取到文本

**解决方案**: 
1. 确保安装了 `opencv-python`
2. 设置 `force_ocr=True` 或 `use_ocr=True`

```bash
pip install opencv-python
```

```python
md_text = pymupdf4llm.to_markdown("scanned.pdf", force_ocr=True)
```

### 问题 3：编码问题

**症状**: 特殊字符显示不正确

**解决方案**: 使用 UTF-8 编码写入文件

```python
import pathlib

# 正确方式
pathlib.Path("output.md").write_bytes(md_text.encode('utf-8'))

# 或
with open("output.md", "w", encoding="utf-8") as f:
    f.write(md_text)
```

## 输出示例

### Markdown 输出示例

```markdown
# Attention Is All You Need

## Abstract
The dominant sequence transduction models are based on complex recurrent or convolutional neural networks ...

## 1. Introduction
...

### 1.1 Background
...
```

### page_chunks 输出示例

```python
[
    {
        "text": "# Title\n\nPage content...",
        "metadata": {
            "page_number": 0,
            "file": "document.pdf"
        },
        "bbox": [0, 0, 612, 792]
    },
    ...
]
```

## 最佳实践

1. **总是先导入 `pymupdf.layout`** 以启用布局模式
2. **使用 `page_chunks=True`** 进行结构化处理
3. **使用 `header=False, footer=False`** 去除重复的页眉页脚
4. **处理大量 PDF 时使用批处理**
5. **使用 LlamaIndex Reader** 直接集成到 RAG 流程

## 命令行用法

```bash
# 转换为 Markdown
python -c "import pymupdf4llm; print(pymupdf4llm.to_markdown('input.pdf'))"

# 批量转换
for f in *.pdf; do python -c "import pymupdf4llm; open('$f'); \
  print(pymupdf4llm.to_markdown('$f'))" > "${f%.pdf}.md"; done
```

## 快速参考表

| 任务 | 代码 |
|------|------|
| 基本转换 | `pymupdf4llm.to_markdown("file.pdf")` |
| 布局模式 | `import pymupdf.layout` + `to_markdown()` |
| 按页提取 | `to_markdown(..., pages=[0,1,2])` |
| 页块输出 | `to_markdown(..., page_chunks=True)` |
| 去页眉页脚 | `to_markdown(..., header=False, footer=False)` |
| 提取图像 | `to_markdown(..., write_images=True)` |
| OCR处理 | `to_markdown(..., force_ocr=True)` |
| JSON输出 | `pymupdf4llm.to_json("file.pdf")` |
| 纯文本 | `pymupdf4llm.to_text("file.pdf")` |
| LlamaIndex | `pymupdf4llm.LlamaMarkdownReader().load_data()` |
