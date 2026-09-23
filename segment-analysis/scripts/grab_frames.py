# -*- coding: utf-8 -*-
"""在指定时间点从视频抽帧，用于核对课件画面（不依赖 ffmpeg，用 PyAV）。

用法：
  python grab_frames.py --source "F:\\path\\lesson.mp4" --out-dir "work" --start-chunk 1 --count 7
  python grab_frames.py --source "F:\\path\\lesson.mp4" --out-dir "work" --seconds 30,300,600,1790

默认在每段起点取帧（--start-chunk 1 --count 7 --chunk-seconds 300 → 0,300,600,...,1800 秒）。
输出：<out-dir>/画面-<秒>.jpg（1280x720）。全程本地。
"""
import argparse
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--out-dir", default="work")
    ap.add_argument("--start-chunk", type=int, default=1)
    ap.add_argument("--count", type=int, default=7, help="取帧数量（含每段起点）")
    ap.add_argument("--chunk-seconds", type=int, default=300)
    ap.add_argument("--seconds", default=None, help="改用显式秒列表，如 30,300,600")
    ap.add_argument("--prefix", default="画面-", help="文件名前缀")
    args = ap.parse_args()

    src = Path(args.source)
    if not src.exists():
        print(f"ERROR 源文件不存在: {src}", flush=True)
        return 2

    try:
        import av
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR 需要 PyAV（pip install av）：{exc}", flush=True)
        return 3

    if args.seconds:
        times = [float(x) for x in args.seconds.split(",")]
    else:
        times = [(args.start_chunk - 1 + i) * args.chunk_seconds for i in range(args.count)]
        times = [t for t in times]

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    container = av.open(str(src))
    done = []
    for t in times:
        container.seek(int(t * 1_000_000))
        got = False
        for frame in container.decode(video=0):
            if frame.time is not None and frame.time >= t:
                target = out / f"{args.prefix}{int(t)}秒.jpg"
                frame.to_image().resize((1280, 720)).save(str(target))
                done.append(target.name)
                got = True
                break
        if not got:
            print(f"WARN {int(t)}s 处未取到画面（接近片尾？）", flush=True)

    print("frames ready: " + ", ".join(done), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
