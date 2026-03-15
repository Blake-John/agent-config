#!/usr/bin/env python3
"""
pymupdf4llm CLI - 最简 PDF 转 Markdown/JSON/Text

Usage:
    python pdf2md.py input.pdf              # 转 Markdown
    python pdf2md.py input.pdf -o out.md   # 指定输出
    python pdf2md.py input.pdf -f json     # 转 JSON
    python pdf2md.py input.pdf -f txt     # 转纯文本
    python pdf2md.py input.pdf -p 1,3-5    # 指定页面
    python pdf2md.py input.pdf --no-head   # 去页眉
    python pdf2md.py input.pdf --no-foot   # 去页脚
    python pdf2md.py "*.pdf" -o ./out/    # 批量处理
"""

import argparse
import sys
from pathlib import Path
import glob

try:
    import pymupdf
    import pymupdf4llm
except ImportError:
    print("Error: pip install pymupdf4llm pymupdf-layout")
    sys.exit(1)

try:
    import pymupdf.layout
except ImportError:
    pass


def main():
    parser = argparse.ArgumentParser(description="pymupdf4llm CLI")
    parser.add_argument("input", nargs="?", help="PDF 文件或 pattern")
    parser.add_argument("-o", "--output", help="输出文件/目录")
    parser.add_argument("-f", "--format", choices=["md", "json", "txt"], default="md", help="输出格式 (default: md)")
    parser.add_argument("-p", "--pages", help="页面: 1,3-5,10-N")
    parser.add_argument("--no-head", dest="header", action="store_false", help="去除页眉")
    parser.add_argument("--no-foot", dest="footer", action="store_false", help="去除页脚")
    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        return

    # 收集文件
    files = glob.glob(args.input) if ('*' in args.input or '?' in args.input) else [args.input]
    if not files:
        print(f"No files: {args.input}")
        return

    # 输出目录
    out_dir = Path(args.output) if args.output and Path(args.output).is_dir() else None

    for f in files:
        try:
            # 构建参数
            kwargs = {"header": args.header, "footer": args.footer}
            
            # 解析页面
            if args.pages:
                pages = []
                for part in args.pages.split(','):
                    part = part.strip()
                    if '-' in part:
                        s, e = part.split('-', 1)
                        s, e = int(s) - 1, (int(e) if e.upper() == 'N' else int(e)) - 1
                        pages.extend(range(s, e + 1))
                    else:
                        pages.append(int(part) - 1)
                kwargs['pages'] = pages

            # 转换
            if args.format == "md":
                content = pymupdf4llm.to_markdown(f, **kwargs)
                ext = ".md"
            elif args.format == "json":
                content = pymupdf4llm.to_json(f, **kwargs)
                ext = ".json"
            else:
                content = pymupdf4llm.to_text(f, **kwargs)
                ext = ".txt"

            # 输出
            if args.output and not out_dir:
                Path(args.output).write_text(content, encoding="utf-8")
                print(f"-> {args.output}")
            elif out_dir:
                out_file = out_dir / (Path(f).stem + ext)
                out_file.write_text(content, encoding="utf-8")
                print(f"-> {out_file}")
            else:
                print(content)

        except Exception as e:
            print(f"Error {f}: {e}")


if __name__ == "__main__":
    main()
