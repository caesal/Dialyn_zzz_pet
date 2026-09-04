#!/usr/bin/env python3
"""Render the reproducible Dialyn preview bundle from extracted v2 frames."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image


ROW_DURATIONS: dict[str, list[int]] = {
    "idle": [280, 110, 110, 140, 140, 320],
    "running-right": [120, 120, 120, 120, 120, 120, 120, 220],
    "running-left": [120, 120, 120, 120, 120, 120, 120, 220],
    "waving": [140, 140, 140, 280],
    "jumping": [140, 140, 140, 140, 280],
    "failed": [140, 140, 140, 140, 140, 140, 140, 240],
    "waiting": [150, 150, 150, 150, 150, 260],
    "running": [120, 120, 120, 120, 120, 220],
    "review": [150, 150, 150, 150, 150, 280],
}

CELL_WIDTH = 192
CELL_HEIGHT = 208


def frame_files(state_dir: Path) -> list[Path]:
    return sorted(path for path in state_dir.glob("*.png") if path.is_file())


def load_state(frames_root: Path, state: str) -> list[Image.Image]:
    files = frame_files(frames_root / state)
    expected = len(ROW_DURATIONS[state])
    if len(files) != expected:
        raise SystemExit(f"{state}: expected {expected} PNG frames, found {len(files)}")

    frames: list[Image.Image] = []
    for path in files:
        with Image.open(path) as image:
            frame = image.convert("RGBA")
        if frame.size != (CELL_WIDTH, CELL_HEIGHT):
            raise SystemExit(f"{path}: expected {CELL_WIDTH}x{CELL_HEIGHT}, got {frame.size}")
        frames.append(frame)
    return frames


def save_gif(frames: list[Image.Image], durations: list[int], output: Path) -> None:
    if len(frames) != len(durations):
        raise ValueError("frame and duration counts differ")
    output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False,
    )


def crop_look_frames(atlas_path: Path) -> list[Image.Image]:
    with Image.open(atlas_path) as opened:
        atlas = opened.convert("RGBA")
    if atlas.size != (1536, 2288):
        raise SystemExit(f"atlas: expected 1536x2288, got {atlas.size}")

    frames: list[Image.Image] = []
    for row in (9, 10):
        for column in range(8):
            left = column * CELL_WIDTH
            top = row * CELL_HEIGHT
            frames.append(atlas.crop((left, top, left + CELL_WIDTH, top + CELL_HEIGHT)))
    return frames


def write_mp4(gif_path: Path, output: Path, ffmpeg_exe: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg_exe,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(gif_path),
            "-r",
            "15",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output),
        ],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames-root", required=True)
    parser.add_argument("--atlas", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--ffmpeg-exe")
    parser.add_argument("--skip-mp4", action="store_true")
    parser.add_argument("--json-out")
    args = parser.parse_args()

    frames_root = Path(args.frames_root).expanduser().resolve()
    atlas_path = Path(args.atlas).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    states = {state: load_state(frames_root, state) for state in ROW_DURATIONS}
    outputs: list[dict[str, object]] = []

    for state, durations in ROW_DURATIONS.items():
        path = output_dir / "states" / f"{state}.gif"
        save_gif(states[state], durations, path)
        outputs.append({"kind": "state", "state": state, "path": str(path), "frames": len(durations)})

    all_frames: list[Image.Image] = []
    all_durations: list[int] = []
    for state, durations in ROW_DURATIONS.items():
        all_frames.extend(states[state])
        all_durations.extend(durations)
    all_states_path = output_dir / "all-states.gif"
    save_gif(all_frames, all_durations, all_states_path)
    outputs.append({"kind": "combined", "path": str(all_states_path), "frames": len(all_frames)})

    transition_frames = states["idle"] + states["jumping"] + states["idle"]
    transition_durations = ROW_DURATIONS["idle"] + ROW_DURATIONS["jumping"] + ROW_DURATIONS["idle"]
    transition_path = output_dir / "idle-jump-idle.gif"
    save_gif(transition_frames, transition_durations, transition_path)
    outputs.append({"kind": "transition", "path": str(transition_path), "frames": len(transition_frames)})

    look_frames = crop_look_frames(atlas_path)
    look_loop = look_frames + [look_frames[0].copy()]
    look_path = output_dir / "look-loop.gif"
    save_gif(look_loop, [120] * len(look_loop), look_path)
    outputs.append({"kind": "look", "path": str(look_path), "frames": len(look_loop)})

    stills = {
        "idle.png": states["idle"][0],
        "jump.png": states["jumping"][2],
        "wave.png": states["waving"][2],
        "look-up.png": look_frames[0],
    }
    for name, image in stills.items():
        path = output_dir / "stills" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path)
        outputs.append({"kind": "still", "path": str(path), "frames": 1})

    if not args.skip_mp4:
        ffmpeg_exe = args.ffmpeg_exe or shutil.which("ffmpeg")
        if not ffmpeg_exe:
            raise SystemExit("ffmpeg was not found; pass --ffmpeg-exe or use --skip-mp4")
        mp4_path = output_dir / "all-states.mp4"
        write_mp4(all_states_path, mp4_path, ffmpeg_exe)
        outputs.append({"kind": "video", "path": str(mp4_path), "frames": len(all_frames), "fps": 15})

    result = {"ok": True, "frames_root": str(frames_root), "atlas": str(atlas_path), "outputs": outputs}
    if args.json_out:
        json_path = Path(args.json_out).expanduser().resolve()
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
