"""本地文档转 Markdown（.docx / .pdf），零联网，不修改源文件。

用法：
    python md_convert.py <输入文件> [-o <输出文件>]
    不带 -o 时直接把 Markdown 打印到屏幕。

依赖：
    pip install mammoth pdfplumber
"""
import argparse
import os
import sys


def convert_docx(path):
    import mammoth
    with open(path, "rb") as f:
        return mammoth.convert_to_markdown(f).value


def convert_pdf(path):
    import pdfplumber
    parts = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = (page.extract_text() or "").strip()
            if text:
                parts.append(f"<!-- 第 {i} 页 -->\n{text}")
            else:
                # 扫描件 / 图片页：提取不到文字，需另行 OCR
                parts.append(f"<!-- 第 {i} 页（无文字/纯图片页） -->")
    return "\n\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description="本地 docx/pdf 转 Markdown（不联网）")
    ap.add_argument("input", help="输入文件路径")
    ap.add_argument("-o", "--output", help="输出 md 文件路径（缺省打印到屏幕）")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(args.input)[1].lower()
    if ext == ".docx":
        md = convert_docx(args.input)
    elif ext == ".pdf":
        md = convert_pdf(args.input)
    else:
        print(f"不支持的类型: {ext}（本脚本支持 .docx / .pdf，其它格式请用 markitdown）",
              file=sys.stderr)
        sys.exit(1)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"已转换: {args.input}\n  -> {args.output}（{len(md)} 字符）")
    else:
        print(md)


if __name__ == "__main__":
    main()
