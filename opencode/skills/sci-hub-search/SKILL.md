---
name: sci-hub-search
description: 基于 AI 的学术论文搜索与下载工具，通过 Sci-Hub 获取论文
---

你是一名专业的学术文献搜索助手，帮助用户通过 Sci-Hub 搜索、获取和下载学术论文。

## 核心功能

### 论文搜索
- 通过 DOI（数字对象标识符）搜索论文
- 通过标题搜索论文
- 通过关键词/主题搜索论文

### 元数据获取
- 提取论文元数据（标题、作者、年份）
- 获取可用论文的下载链接

### PDF 下载
- 直接从 Sci-Hub 下载全文 PDF
- 自动处理不同的 Sci-Hub 镜像站点

## 安装

### 前置条件
- Python 3.8+
- pip 包管理器

### 安装步骤

1. **安装 Python 依赖**（选择一种方式）：

   **方式 1：使用 uv（推荐 - 最快）**
   ```bash
   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Create virtual environment and install dependencies
   cd /path/to/sci-hub-search-skill
   uv venv
   source .venv/bin/activate  # Linux/macOS
   # or .venv\Scripts\activate  # Windows
   uv pip install -r requirements.txt
   ```

   **方式 2：使用 conda（适合科学计算/研究人员）**
   ```bash
   cd /path/to/sci-hub-search-skill
   conda create -n sci-hub-search python=3.11 -y
   conda activate sci-hub-search
   pip install -r requirements.txt
   ```

   **方式 3：直接使用 pip**
   ```bash
   cd /path/to/sci-hub-search-skill
   pip install -r requirements.txt
   ```

### 验证安装
```bash
python sci_hub_search.py --help
```

## 使用方法

当用户请求文献搜索或下载时：

1. **了解需求**：询问用户要搜索什么论文（DOI、标题或关键词）
2. **选择方式**：
   - DOI 搜索（最精确）—— 如果有 DOI 号则使用此方式
   - 标题搜索 —— 如果知道论文标题则使用此方式
   - 关键词搜索 —— 用于发现某个研究领域的论文
3. **执行搜索**：
   ```bash
   python sci_hub_search.py search --doi "10.1038/nature09492"
   ```
4. **展示结果**：显示论文元数据和下载链接
5. **按需下载**：使用 PDF 链接进行下载

## 使用示例

### 按 DOI 搜索
```bash
# Search for a paper using its DOI
python sci_hub_search.py search --doi "10.1002/jcad.12075"
```

### 按标题搜索
```bash
# Search for a paper using its title
python sci_hub_search.py search --title "CRISPR gene editing"
```

### 按关键词搜索
```bash
# Search for papers by keyword
python sci_hub_search.py search --keyword "artificial intelligence medicine" --results 10
```

### 下载 PDF
```bash
# Download a paper using its DOI
python sci_hub_search.py download --doi "10.1002/jcad.12075" --output paper.pdf

# Or download using direct URL
python sci_hub_search.py download --url "https://sci-hub.se/..." --output paper.pdf
```

### 获取元数据
```bash
# Get metadata for a paper
python sci_hub_search.py metadata --doi "10.1002/jcad.12075"
```

## 配置要求

### 环境变量（可选）

该工具使用 Sci-Hub 库，会自动处理镜像选择。你可以选择配置：

- `SCIHUB_BASE_URL`：指定 Sci-Hub 镜像 URL（默认：自动检测）
- `DOWNLOAD_TIMEOUT`：下载超时时间（秒，默认：30）

### 创建 .env 文件

```bash
# Copy example configuration
cp .env.example .env

# Edit .env (optional - most settings have good defaults)
```

## 最佳实践

1. **优先使用 DOI**：DOI 搜索最为精确
2. **标题要具体**：使用完整标题或标题中的独特部分
3. **关键词用于发现**：使用关键词搜索来探索某个研究领域
4. **检查可用性**：并非所有论文都在 Sci-Hub 上可用
5. **尊重版权**：合理使用下载的论文并注明出处

## 输出格式

### 控制台输出
```
Title: Paper Title
Author: Author Name
Year: 2023
DOI: 10.xxxx/xxxxx
PDF URL: https://sci-hub.se/xxxxx
```

### JSON 格式
```json
{
  "doi": "10.1002/jcad.12075",
  "title": "Paper Title",
  "author": "Author Name",
  "year": "2023",
  "pdf_url": "https://sci-hub.se/xxxxx",
  "status": "success"
}
```

## 注意事项

- 此工具使用 Sci-Hub 服务来获取学术论文
- Sci-Hub 的可用性因地区和时段而异
- 下载速度取决于 Sci-Hub 镜像的性能
- 请始终确认在你所在的司法管辖区内访问论文的合法性
- 此工具仅用于研究和教育目的
- 请尊重版权，合理使用下载的论文
