# segment-analysis · 长视频逐段分析（每 5 分钟一段）

把长课程 / 长视频做成"每 5 分钟一段"的逐段分析：**先本地转写＋抽帧取真材料，再逐段写「内容／分析／对照与处理」，最后与旧笔记查缺补漏。**

一句话：长材料不能一口吞——按 5 分钟切段，每段都要回答"这段讲了什么 / 这意味着什么 / 原有笔记要不要改"。

## 快速开始

```powershell
pip install faster-whisper av

# 1) 每 5 分钟一段，本地转写（不依赖 ffmpeg，直接读 mp4）
python scripts/transcribe_chunks.py --source "lesson.mp4" --out-dir work --start-chunk 1 --count 6

# 2) 每段起点抽一帧，用来核对课件画面
python scripts/grab_frames.py --source "lesson.mp4" --out-dir work --start-chunk 1 --count 7
```

一轮 30 分钟＝6 段，CPU 约 1 分钟/段。产出 `segment-N.json` 与 `画面-<秒>.jpg`。

## 为什么不是"直接让 AI 总结"

- **切段**：一次给模型全片会糊，5 分钟粒度才看得出"哪一段在讲什么"。
- **抽帧**：课件上的大字常是全片最可靠的锚点，防止把转写错字当成原话。
- **对照**：每段都必须回答"旧笔记有没有、要不要补"——没有对照就没有补漏。
- **证据纪律**：讲者自述的成效不作规律；课件显示了但没讲到的提纲不算"已讲内容"。

## 目录

- [`SKILL.md`](SKILL.md) — 五条铁律、完整流程、证据纪律、自检清单、踩过的坑
- [`references/report-template.md`](references/report-template.md) — 报告与来源说明的骨架、交付汇报格式
- [`references/prompt.md`](references/prompt.md) — 可整段粘贴给其它 AI 的提示词
- [`scripts/transcribe_chunks.py`](scripts/transcribe_chunks.py) — 按固定时长切段并本地转写
- [`scripts/grab_frames.py`](scripts/grab_frames.py) — 指定时间点抽帧（PyAV）
