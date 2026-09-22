---
name: doc-convert
description: 把 docx / pdf / pptx / xlsx / 音视频等本地文件转成 Markdown，便于 AI 理解与归档；不修改源文件、默认不联网上传。适用于"转 md""读 word/pdf/ppt/excel""把资料转成文字"等场景。
---

# 文档转 Markdown（本地转换，不碰源文件）

把非 Markdown 的资料转成 Markdown，方便阅读、检索与归档。三条原则：

1. **本地转换**——默认不把文件传给任何云端服务。
2. **不碰源文件**——只读源文件，产物另存。
3. **转完必须读回确认**——不读回就等于没转。

## 什么时候用

- 收到 docx / pdf / pptx / xlsx / 音视频等文件，想"转成文字 / md / 看得懂"。
- 想让 AI 读完**整份资料**再回答，而不是只看文件名猜内容。
- 把历史资料（报告、课件、扫描件）沉淀成可检索、可搜索的文本。

## 工具选择

| 目标格式 | 工具 | 说明 |
|---|---|---|
| docx / pdf | `scripts/md_convert.py` | 本地转换（mammoth / pdfplumber），零联网 |
| pptx / xlsx / 音视频 / 网页 | `markitdown` CLI | 覆盖面更广的通用方案 |

装依赖（**只用 pip 官方方式，不要自己写装包脚本**）：

```powershell
pip install mammoth pdfplumber          # md_convert.py 需要
pip install "markitdown[all]"           # 通用方案，按需
```

> 真实教训：曾手写脚本去解析依赖，跑了十几个小时、拖进 7000+ 个无关包、占掉 43GB 磁盘。
> 正确做法永远是 `pip install "包[extras]"`。

## 步骤

### 1. docx / pdf → Markdown

```powershell
python scripts/md_convert.py "<输入文件>" -o "<输出.md>"
```

- 不带 `-o` 会直接把 Markdown 打印到屏幕，适合先扫一眼内容。
- 文件不存在或类型不支持时，脚本会报错退出，不会产生半成品。

### 2. 其它格式 → Markdown

```powershell
markitdown path\to\file.pptx > out.md
```

音视频转换依赖 `ffmpeg`；缺 ffmpeg 只影响音视频，不影响文档类。

### 3. 读回确认（必做）

- 内容完整、无乱码、无整段丢失。
- **纯图片页**：扫描件 PDF 用 `pdfplumber` 提取不到文字，脚本会为该页标注
  `<!-- 第 N 页（无文字/纯图片页） -->`。看到这种标注说明这一页要单独走 OCR 流程，
  **不能当成"已经转完了"**。

## 常见坑

- 别自己写装包脚本，第三方库只用 pip / 官方方式。
- 中文或带空格的路径先复制到纯英文目录再转换，避免命令行参数乱码。
- 扫描件 / 拍照件属于图片，转不出文字，需要 OCR（见 `handwritten-diary-ocr`）。
- 转换产物要归档到固定目录，别丢在临时目录里找不到。

## 验收清单

- [ ] 读回生成的 md，逐段比对源文件，无乱码、无缺页
- [ ] 页数 / 章节数与源文件一致
- [ ] 纯图片页有明确标注，并已决定是否走 OCR
- [ ] 源文件未被修改（对比文件修改时间）
