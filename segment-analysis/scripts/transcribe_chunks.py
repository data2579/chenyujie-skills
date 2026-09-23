# -*- coding: utf-8 -*-
"""按固定时长把长视频/音频切成片段并本地转写（默认每 5 分钟一段）。

用法：
  python transcribe_chunks.py --source "F:\\path\\lesson.mp4" --out-dir "work" --start-chunk 1 --count 6
  python transcribe_chunks.py --source "F:\\path\\lesson.mp4" --out-dir "work" --range 3570,5390

输出：<out-dir>/segment-<N>.json，N 是从视频开头算起的第 N 段（1 基），
      内容为 [{"start": 秒, "end": 秒, "text": "..."}]，保留识别原貌（不要在 json 里改字）。

说明：不依赖 ffmpeg；faster-whisper 直接读 mp4。全程本地，不上传。
"""
import argparse
import json
import sys
import time
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="视频/音频文件绝对路径")
    ap.add_argument("--out-dir", default="work", help="输出目录")
    ap.add_argument("--start-chunk", type=int, default=1, help="起始段号（1 基，从视频开头算）")
    ap.add_argument("--count", type=int, default=6, help="转写段数")
    ap.add_argument("--chunk-seconds", type=int, default=300, help="每段秒数，默认 300（5 分钟）")
    ap.add_argument("--range", default=None, help="改用绝对秒范围 'start,end'（覆盖 start-chunk/count）")
    ap.add_argument("--model", default="base", help="faster-whisper 模型名，默认 base")
    ap.add_argument("--language", default="zh", help="语言，默认 zh")
    ap.add_argument("--threads", type=int, default=8, help="CPU 线程数")
    args = ap.parse_args()

    src = Path(args.source)
    if not src.exists():
        print(f"ERROR 源文件不存在: {src}", flush=True)
        return 2

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # 延迟导入，便于在缺依赖时给出清晰提示
    try:
        from faster_whisper import WhisperModel
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR 需要 faster-whisper（pip install faster-whisper）：{exc}", flush=True)
        return 3

    if args.range:
        start_all, end_all = (float(x) for x in args.range.split(","))
        jobs = []
        cur = start_all
        idx = int(start_all // args.chunk_seconds) + 1
        while cur < end_all:
            jobs.append((idx, cur, min(cur + args.chunk_seconds, end_all)))
            cur += args.chunk_seconds
            idx += 1
    else:
        jobs = []
        for i in range(args.count):
            index = args.start_chunk + i
            start = (index - 1) * args.chunk_seconds
            jobs.append((index, start, start + args.chunk_seconds))

    print(f"模型={args.model} 段数={len(jobs)} 输出={out}", flush=True)
    t0 = time.time()
    model = WhisperModel(args.model, device="cpu", compute_type="int8",
                         local_files_only=True, cpu_threads=args.threads)

    for index, start, end in jobs:
        segments, _info = model.transcribe(
            str(src),
            language=args.language,
            beam_size=5,
            clip_timestamps=f"{int(start)},{int(end)}",
            condition_on_previous_text=False,
        )
        data = []
        for seg in segments:
            if seg.start >= end:
                break
            data.append({"start": round(seg.start, 3), "end": round(seg.end, 3),
                         "text": seg.text.strip()})
        (out / f"segment-{index}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"FINISHED {index} {len(data)} 段  {int(start)//60:02d}:{int(start)%60:02d}"
              f"-{int(end)//60:02d}:{int(end)%60:02d}", flush=True)

    print(f"全部完成，耗时 {time.time() - t0:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
