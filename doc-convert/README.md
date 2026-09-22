# doc-convert · 文档转 Markdown

把 docx / pdf / pptx / xlsx / 音视频等本地文件转成 Markdown，便于 AI 读懂与归档。

**三条原则**：本地转换 · 不碰源文件 · 默认不联网上传。

## 快速开始

```powershell
pip install mammoth pdfplumber

# docx / pdf → Markdown
python scripts/md_convert.py "报告.docx" -o "报告.md"

# 其它格式（pptx / xlsx / 音视频等）
pip install "markitdown[all]"
markitdown 课件.pptx > 课件.md
```

## 目录

- [`SKILL.md`](SKILL.md) — 完整流程、坑与验收清单（给 AI 读的技能文件）
- [`scripts/md_convert.py`](scripts/md_convert.py) — docx / pdf → Markdown，零联网、不动源文件

> 扫描件 PDF 属于图片，提取不到文字，会标注"纯图片页"，需要另走 OCR（见 `handwritten-diary-ocr`）。
