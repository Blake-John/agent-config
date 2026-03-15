---
name: pymupdf
description: >
  使用 PyMuPDF4LLM 处理 PDF 文献。当用户提到提取 PDF 文本、转换 PDF 为 Markdown、从 PDF 提取表格、将 PDF 转换为 JSON、处理扫描版 PDF、或需要将 PDF 文档准备用于 RAG/LLM 应用时，必须使用此 skill。
compatibility:
  tools:
    - bash
    - write
    - read
    - glob
  dependencies:
    - pymupdf4llm
    - pymupdf-layout
---

# PyMuPDF4LLM

将 PDF 转换为 LLM 易读的 Markdown/JSON/Text 格式。

## 安装

```bash
pip install pymupdf4llm pymupdf-layout
```

## CLI 命令

脚本: `./scripts/pdf2md.py`

```bash
# PDF -> Markdown (最常用)
python ./scripts/pdf2md.py input.pdf -o output.md

# PDF -> JSON (含布局信息)
python ./scripts/pdf2md.py input.pdf -f json -o output.json

# PDF -> TXT
python ./scripts/pdf2md.py input.pdf -f txt -o output.txt

# 指定页面
python ./scripts/pdf2md.py input.pdf -p 1,3-5 -o output.md

# 去除页眉页脚
python ./scripts/pdf2md.py input.pdf --no-head --no-foot -o output.md

# 批量处理
python ./scripts/pdf2md.py "*.pdf" -o ./output/

# 查看帮助
python ./scripts/pdf2md.py -h
```

## Python API

官方文档最简用法：

```python
import pymupdf4llm

# Markdown (推荐)
md = pymupdf4llm.to_markdown("input.pdf")
Path("output.md").write_bytes(md.encode())

# JSON (含边界框和布局)
json = pymupdf4llm.to_json("input.pdf")

# 纯文本
txt = pymupdf4llm.to_text("input.pdf")

# 去除页眉页脚
md = pymupdf4llm.to_markdown("input.pdf", header=False, footer=False)

# 指定页面 (0-based)
md = pymupdf4llm.to_markdown("input.pdf", pages=[0, 1, 2])
```

## 选项说明

| CLI 参数 | Python 参数 | 说明 |
|----------|-------------|------|
| `-f md/json/txt` | `to_markdown/to_json/to_text` | 输出格式 |
| `-p 1,3-5` | `pages=[0,1,2,3,4]` | 页面 (CLI 1-based, API 0-based) |
| `--no-head` | `header=False` | 去除页眉 |
| `--no-foot` | `footer=False` | 去除页脚 |

## 常用任务

```python
# 批量转换
import pymupdf4llm
from pathlib import Path

for pdf in Path(".").glob("*.pdf"):
    md = pymupdf4llm.to_markdown(str(pdf))
    pdf.with_suffix(".md").write_bytes(md.encode())

# LlamaIndex 集成
import pymupdf4llm
reader = pymupdf4llm.LlamaMarkdownReader()
docs = reader.load_data("input.pdf")

# LangChain 集成
from langchain_community.document_loaders import PyMuPDFLoader
loader = PyMuPDFLoader("input.pdf")
docs = loader.load()
```
